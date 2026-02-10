import requests
from concurrent.futures import ThreadPoolExecutor

COMMON_FILES = [
    ".env", ".git/config", "config.php", "wp-config.php", "backup.zip",
    "dashboard", "api", "admin", "robots.txt", "sitemap.xml",
    "id_rsa", ".ssh/id_rsa", "docker-compose.yml"
]

def check_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=3, allow_redirects=False)
        if res.status_code == 200:
            return (url, res.status_code, len(res.content))
    except:
        pass
    return None

def run_fuzzer(target):
    print(f"   [*] Starting sensitive file fuzzing on {target}...")
    found_paths = []
    
    # 1. Load Wordlists (if large, we'd stream them, but these are small)
    # For now, we extend COMMON_FILES with some critical ones to ensure value even without full wordlists
    # In a full tool, you'd load from the wordlists/ directory
    
    base_url = f"http://{target}"
    urls_to_check = [f"{base_url}/{path}" for path in COMMON_FILES]
    
    # Also check HTTPS
    base_url_ssl = f"https://{target}"
    urls_to_check.extend([f"{base_url_ssl}/{path}" for path in COMMON_FILES])

    # OPTIMIZATION: Increased threads from 10 to 50 for speed
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_url, urls_to_check)
        
        for result in results:
            if result:
                url, status, size = result
                print(f"   [!] FOUND: {url} (Status: {status}, Size: {size})")
                found_paths.append({"url": url, "status": status, "size": size})
    
    if not found_paths:
        print("   [+] No obvious sensitive files found.")
                
    return found_paths
