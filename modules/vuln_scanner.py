import requests
import re
import urllib3
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_vuln_scan(target, recon_data, crawl_paths=[]):
    print(f"   [*] Starting Vulnerability Scan on {target}...")
    vulns = []
    
    # 1. Subdomain Takeover Check
    print("   [*] Checking for Subdomain Takeover risks...")
    cnames = recon_data.get("dns_records", {}).get("CNAME", [])
    
    # Fingerprints for common services
    takeover_signatures = {
        "github.io": "There isn't a GitHub Pages site here.",
        "herokuapp.com": "No such app",
        "amazonaws.com": "The specified bucket does not exist",
        "azurewebsites.net": "404 Web Site not found",
        "unbouncepages.com": "The requested URL was not found on this server"
    }
    
    # Check subdomains found in recon
    subdomains = recon_data.get("subdomains", [target])
    for sub in subdomains:
        try:
            # Resolve CNAME (simplified, assuming we might need to resolve again or use recon data if detailed)
            # For now, let's just check HTTP response text for signatures if we can't easily get CNAMEs for all
            url = f"http://{sub}"
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                res = requests.get(url, headers=headers, timeout=5, verify=False)
                for domain, signature in takeover_signatures.items():
                    if signature in res.text:
                        print(f"   [!] POTENTIAL TAKEOVER: {sub} (matched {domain})")
                        vulns.append({"type": "Subdomain Takeover", "target": sub, "details": f"Matched signature for {domain}"})
            except:
                pass
        except:
            pass

    # 2. CORS Misconfiguration
    print(f"   [*] Checking CORS configuration on https://{target}...")
    try:
        url = f"https://{target}"
        origin = "https://evil.com"
        headers = {"Origin": origin}
        res = requests.get(url, headers=headers, timeout=5)
        
        if res.headers.get("Access-Control-Allow-Origin") == origin:
            if res.headers.get("Access-Control-Allow-Credentials") == "true":
                print(f"   [!] CRITICAL: CORS Misconfiguration found on {url} (Allows Credentials)")
                vulns.append({"type": "CORS Misconfiguration", "url": url, "severity": "High"})
            else:
                print(f"   [!] INFO: CORS Allow-Origin reflects input on {url}")
                vulns.append({"type": "CORS Reflection", "url": url, "severity": "Low"})
    except:
        pass

    # 3. Sensitive Information Disclosure (New)
    print(f"   [*] Checking for Sensitive Information exposure...")
    
    sensitive_paths = [
        "/.git/HEAD",
        "/.env",
        "/.svn/entries",
        "/phpinfo.php",
        "/info.php",
        "/server-status"
    ]
    
    base_url = f"https://{target}"
    
    for path in sensitive_paths:
        test_url = f"{base_url}{path}"
        try:
            res = requests.get(test_url, timeout=5, verify=False, allow_redirects=False)
            
            is_vuln = False
            details = ""
            
            if path == "/.git/HEAD" and "ref: refs/heads" in res.text:
                is_vuln = True
                details = "Exposed .git repository (Source Code Leak)"
            elif path == "/.env" and "DB_PASSWORD" in res.text:
                is_vuln = True
                details = "Exposed .env file (Credential Leak)"
            elif "phpinfo()" in res.text and res.status_code == 200:
                is_vuln = True
                details = "Exposed phpinfo() (Configuration Leak)"
            elif path == "/server-status" and "Apache Status" in res.text:
                is_vuln = True
                details = "Exposed Apache Server Status"

            if is_vuln:
                print(f"   [!] CRITICAL VULN: {details} at {test_url}")
                vulns.append({
                    "type": "Sensitive Info Leak",
                    "url": test_url,
                    "details": details
                })
        except:
            pass

    return vulns

def check_cors(target):
    print(f"   [*] Checking CORS configuration on https://{target}...")
    vulns = []
    headers = {
        'Origin': 'https://evil.com'
    }
    try:
        res = requests.get(f"https://{target}", headers=headers, timeout=5, verify=False)
        if 'Access-Control-Allow-Origin' in res.headers:
            acao = res.headers['Access-Control-Allow-Origin']
            if acao == 'https://evil.com' or acao == '*' or acao == 'null':
                
                # Step 2: Verify Credentials Impact
                acac = res.headers.get('Access-Control-Allow-Credentials', 'false')
                severity = "HIGH" if acac == 'true' and acao != '*' else "MEDIUM"
                
                details = f"Origin reflected: {acao}, Credentials: {acac}"
                print(f"   [!] VULN: CORS Misconfiguration ({severity}) on {target}")
                print(f"       Details: {details}")
                
                vulns.append({
                    "type": f"CORS Misconfiguration ({severity})",
                    "url": f"https://{target}",
                    "details": details
                })
    except:
        pass
    return vulns
