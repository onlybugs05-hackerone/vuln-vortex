# VULN-VORTEX 🌪️

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

**Advanced Bug Bounty & Reconnaissance Framework**  
*Forged by OnlyBugs05*

> **Warning**: This tool is for educational purposes and authorized security testing only. Misuse may be illegal.

**Vuln-Vortex** is a high-speed, automated reconnaissance and vulnerability scanning suite designed for modern bug bounty hunters. It combines multi-threaded enumeration, smart fuzzing, and vulnerability detection into a single "God Mode" tool.

## 🚀 Key Features

- **⚡ Turbo Recon**: 
  - Subdomain enumeration via Certificate Transparency (crt.sh).
  - Multi-threaded IP resolution and DNS analysis.
  
- **🛡️ WAF & Tech Detection**: 
  - Identifies Cloudflare, AWS WAF, Akamai, etc.
  - Fingerprints CMS (WordPress, Joomla, Drupal) and Server headers.

- **🔍 Smart Scanning**:
  - **Port Scanner**: 100-threaded scanner for top 1000 ports.
  - **Fuzzer**: 50-threaded sensitive file discovery (`.env`, `.git`, `backup.zip`).

- **🔓 Advanced Vulnerability Engine**:
  - **Open Redirects**: Features **2-Step Verification** to follow redirects and confirm destination (reduces false positives).
  - **CORS Misconfiguration**: Detects reflected Origins and Credential leakage.
  - **Subdomain Takeover**: Checks for dangling CNAME records (S3, GitHub Pages, Heroku).

- **📊 Cyberpunk Dashboard**: 
  - Auto-generates a stunning, interactive HTML report (`report.html`) with dark mode UI.

## 📦 Installation

Works on Kali Linux, Parrot OS, Ubuntu, and Debian.

```bash
# Clone the repository
git clone https://github.com/OnlyBugs05-hackerone/vuln-vortex.git

# Navigate to directory
cd vuln-vortex

# Run the installer (sets up venv & dependencies)
chmod +x install.sh
./install.sh
```

## ⚔️ Usage

### 🟢 Interactive Mode (Recommended)
Just run the tool without arguments to use the menu system:
```bash
./vortex
```

### 🔴 Direct Mode (CLI)
For quick scans or scripting:
```bash
./vortex <target.com>
```

### ⚙️ advanced Options
```bash
./vortex -t example.com --mode full    # Complete Audit (Recon + Scan + Fuzz + Vuln)
./vortex -t example.com --mode recon   # Only Reconnaissance
./vortex -t example.com --mode scan    # Port & Header Scan
./vortex -t example.com --mode fuzz    # Sensitive File Fuzzing
./vortex -t example.com --mode vuln    # Vulnerability Checks
```

## 📄 HTML Reports
After every scan, a `report.html` file is generated in the current directory. Open it in your browser to view the results:

```bash
xdg-open report.html
```

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/OnlyBugs05-hackerone/vuln-vortex/issues).

## 📜 License
Distrubuted under the MIT License. See `LICENSE` for more information.

---
*Made with ❤️ by OnlyBugs05*
