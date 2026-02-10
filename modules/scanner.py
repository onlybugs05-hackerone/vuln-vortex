import requests
import socket

def run_scan(target, recon_data):
    scan_results = {
        "headers": {},
        "open_ports": []
    }
    
    # 1. Check HTTP Headers
    url = f"https://{target}"
    print(f"   [*] Analyzing headers for {url}...")
    try:
        headers_ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers_ua, timeout=5)
        headers = response.headers
        
        security_headers = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "X-Content-Type-Options"
        ]
        
        missing = []
        for h in security_headers:
            if h not in headers:
                missing.append(h)
            else:
                scan_results["headers"][h] = headers[h]
        
        scan_results["missing_headers"] = missing
        if missing:
            print(f"   [!] Missing Security Headers: {', '.join(missing)}")
        else:
            print("   [+] All key security headers present.")
            
    except requests.exceptions.RequestException as e:
        print(f"   [-] Failed to connect to {url}: {e}")

    # 2. Multi-threaded Port Scan
    target_ip = recon_data.get("ip_addresses", [None])[0]
    
    if target_ip:
        # Extended port list for "useful" scanning
        ports_to_scan = [
            21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 
            993, 995, 1433, 1723, 3306, 3389, 5900, 8000, 8080, 8443
        ]
        print(f"   [*] Fast-scanning {len(ports_to_scan)} common ports on {target_ip}...")
        
        import concurrent.futures
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1) # 1 second timeout
                result = sock.connect_ex((target_ip, port))
                sock.close()
                if result == 0:
                    return port
            except:
                pass
            return None

        # OPTIMIZATION: Massive concurrency boost for port scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(check_port, ports_to_scan)
            
            for port in results:
                if port:
                    scan_results["open_ports"].append(port)
                    print(f"   [+] Port {port} is OPEN")
            
    return scan_results
