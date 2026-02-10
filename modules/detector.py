import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_detector(target):
    print(f"   [*] Detect Tech Stack & WAF on {target}...")
    tech_info = {
        "waf": None,
        "server": None,
        "cms": None,
        "frameworks": []
    }
    
    url = f"https://{target}"
    try:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=5, verify=False)
        
        # 1. Analyze Headers
        srv = res.headers.get("Server", "")
        powered = res.headers.get("X-Powered-By", "")
        via = res.headers.get("Via", "")
        
        if srv: tech_info["server"] = srv
        if powered: tech_info["frameworks"].append(powered)
        
        # 2. WAF Detection
        if "cloudflare" in srv.lower() or "__cfduid" in res.cookies:
            tech_info["waf"] = "Cloudflare"
        elif "awselb" in res.cookies or "AWSALB" in res.cookies:
            tech_info["waf"] = "AWS ELB/WAF"
        elif "Akamai" in via:
            tech_info["waf"] = "Akamai"
        
        # 3. CMS/Framework Detection (Body Analysis)
        body = res.text.lower()
        if "wp-content" in body or "wordpress" in body:
            tech_info["cms"] = "WordPress"
        elif "joomla" in body:
            tech_info["cms"] = "Joomla"
        elif "drupal" in body:
            tech_info["cms"] = "Drupal"
        elif "shopify" in body:
            tech_info["cms"] = "Shopify"
            
        if "react" in body: tech_info["frameworks"].append("React")
        if "vue" in body: tech_info["frameworks"].append("Vue.js")
        if "angular" in body: tech_info["frameworks"].append("Angular")
        if "laravel" in body: tech_info["frameworks"].append("Laravel")
        if "django" in body: tech_info["frameworks"].append("Django")
        
        # Clean up
        if tech_info["waf"]:
             from colorama import Fore, Style
             print(f"   {Fore.RED}[!] WAF DETECTED: {tech_info['waf']}{Style.RESET_ALL}")
        if tech_info["server"]:
             print(f"   [+] Server: {tech_info['server']}")
        if tech_info["cms"]:
             from colorama import Fore, Style
             print(f"   {Fore.GREEN}[+] CMS DETECTED: {tech_info['cms']}{Style.RESET_ALL}")
             
    except Exception as e:
        print(f"   [-] Detection failed: {e}")
        
    return tech_info
