import socket
import requests
import dns.resolver
import sys

def run_recon(target):
    recon_data = {
        "target": target,
        "ip_addresses": [],
        "subdomains": [], # In a real tool, we'd integrate subfinder/amass here
        "dns_records": {}
    }
    
    # 1. IP Resolution
    try:
        ais = socket.getaddrinfo(target, 0, 0, 0, 0)
        for result in ais:
            ip = result[-1][0]
            if ip not in recon_data["ip_addresses"]:
                recon_data["ip_addresses"].append(ip)
        print(f"   [+] Found IPs: {', '.join(recon_data['ip_addresses'])}")
    except socket.gaierror:
        print("   [-] Could not resolve target IP.")

    # 1.5. Subdomain Enumeration via CRT.sh
    print(f"   [*] Querying crt.sh for subdomains...")
    try:
        url = f"https://crt.sh/?q=%.{target}&output=json"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            for entry in data:
                name_value = entry['name_value']
                subdomains = name_value.split('\n')
                for sub in subdomains:
                    if sub not in recon_data["subdomains"] and '*' not in sub:
                         recon_data["subdomains"].append(sub)
            print(f"   [+] Found {len(recon_data['subdomains'])} unique subdomains from CRT.sh")
    except Exception as e:
        print(f"   [-] CRT.sh lookup failed: {e}")

    # 2. Basic DNS Records (A, MX, TXT)
    resolver = dns.resolver.Resolver()
    for rtype in ['A', 'MX', 'TXT']:
        try:
            answers = resolver.resolve(target, rtype)
            recon_data["dns_records"][rtype] = [r.to_text() for r in answers]
            print(f"   [+] Found {len(answers)} {rtype} records")
        except:
            pass
            
    return recon_data
