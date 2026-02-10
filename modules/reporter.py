import json
import os
from datetime import datetime

def generate_html_report(json_file="report.json", output_file="report.html"):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except:
        print("[-] Could not load report.json")
        return

    req_count = len(data.get("scan", {}).get("missing_headers", []))
    sub_count = len(data.get("recon", {}).get("subdomains", []))
    vuln_count = len(data.get("vuln", []))
    
    # Prepare HTML chunks outside the f-string to avoid syntax errors
    vulns_html = ""
    if data.get('vuln'):
        rows = ''.join([f'<tr><td><span class="tag danger">{v.get("type")}</span></td><td>{v.get("url") or v.get("target")}</td></tr>' for v in data.get('vuln', [])])
        vulns_html = f"<table><tr><th>Type</th><th>Details</th></tr>{rows}</table>"
    else:
        vulns_html = "<p style='color: var(--success)'>✅ No critical vulnerabilities found in this scan.</p>"

    fuzz_html = ""
    if data.get('fuzz'):
        rows = ''.join([f'<tr><td><a href="{f.get("url")}" style="color: #58a6ff">{f.get("url")}</a></td><td>{f.get("status")}</td><td>{f.get("size")}</td></tr>' for f in data.get('fuzz', [])])
        fuzz_html = f"<table><tr><th>URL</th><th>Status</th><th>Size</th></tr>{rows}</table>"
    else:
        fuzz_html = "<p>No sensitive files found.</p>"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GOD MODE REPORT - {data.get('recon', {}).get('target', 'Unknown')}</title>
        <style>
            :root {{
                --bg: #0d1117;
                --card: #161b22;
                --text: #c9d1d9;
                --accent: #58a6ff;
                --danger: #f85149;
                --success: #238636;
                --warning: #d29922;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 20px;
            }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1, h2, h3 {{ color: var(--accent); }}
            .header {{
                text-align: center;
                padding: 40px 0;
                border-bottom: 2px solid var(--card);
                margin-bottom: 40px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: var(--card);
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #30363d;
            }}
            .stat-number {{ font-size: 2.5em; font-weight: bold; color: var(--text); }}
            .stat-label {{ color: #8b949e; margin-top: 5px; }}
            
            .section {{
                background: var(--card);
                padding: 25px;
                margin-bottom: 25px;
                border-radius: 8px;
                border: 1px solid #30363d;
            }}
            .tag {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                margin: 2px;
                background: #1f6feb;
                color: white;
            }}
            .tag.danger {{ background: var(--danger); }}
            .tag.warning {{ background: var(--warning); color: #000; }}
            
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ 
                padding: 12px; 
                text-align: left; 
                border-bottom: 1px solid #30363d; 
            }}
            th {{ color: #8b949e; }}
            code {{
                background: rgba(110, 118, 129, 0.4);
                padding: 2px 6px;
                border-radius: 4px;
                font-family: monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚡ GOD MODE REPORT ⚡</h1>
                <p>Target: <strong>{data.get('recon', {}).get('target', 'N/A')}</strong> | Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{sub_count}</div>
                    <div class="stat-label">Subdomains</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" style="color: var(--danger)">{vuln_count}</div>
                    <div class="stat-label">Vulnerabilities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" style="color: var(--warning)">{req_count}</div>
                    <div class="stat-label">Missing Headers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{data.get('tech', {}).get('waf', 'None')}</div>
                    <div class="stat-label">WAF Detected</div>
                </div>
            </div>

            <div class="section">
                <h2>🌍 Reconnaissance</h2>
                <h3>IP Addresses</h3>
                <p>{', '.join(data.get('recon', {}).get('ip_addresses', []))}</p>
                
                <h3>Subdomains</h3>
                <div class="tags">
                    {''.join([f'<span class="tag">{sub}</span>' for sub in data.get('recon', {}).get('subdomains', [])])}
                </div>
            </div>

            <div class="section">
                <h2>🛡️ Tech Stack</h2>
                <p><strong>Server:</strong> {data.get('tech', {}).get('server', 'Unknown')}</p>
                <p><strong>CMS:</strong> {data.get('tech', {}).get('cms', 'None')}</p>
                <p><strong>WAF:</strong> <span class="tag danger">{data.get('tech', {}).get('waf', 'None')}</span></p>
            </div>

            <div class="section">
                <h2>🚨 Security Issues</h2>
                <h3>Missing Headers</h3>
                <ul>
                    {''.join([f'<li><code>{h}</code></li>' for h in data.get('scan', {}).get('missing_headers', [])])}
                </ul>
                
                <h3>Open Ports</h3>
                <p>{', '.join([str(p) for p in data.get('scan', {}).get('open_ports', [])]) if data.get('scan', {}).get('open_ports') else "No open ports found (top common list)."}</p>
            </div>

            <div class="section">
                 <h2>🔥 Vulnerabilities Found</h2>
                 {vulns_html}
            </div>
            
             <div class="section">
                 <h2>📂 Fuzzing Results</h2>
                 {fuzz_html}
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html)
    print(f"   [+] HTML Report generated: {output_file}")
