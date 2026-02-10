#!/bin/bash
# Public Installer for VULN-VORTEX
# Works on Kali, Parrot, Ubuntu, Debian

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}    VULN-VORTEX PUBLIC INSTALLER       ${NC}"
echo -e "${BLUE}=======================================${NC}"

# 1. Dependency Check
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[-] Python3 is missing! Please install it.${NC}"
    exit 1
fi

# 2. Reset Environment (Clean State)
if [ -d "venv" ]; then
    echo -e "${BLUE}[*] Cleaning up old environment...${NC}"
    rm -rf venv
fi

# 3. Create Fresh Virtual Environment
echo -e "${GREEN}[*] Setting up Python Environment...${NC}"
python3 -m venv venv

# 4. Install Dependencies
echo -e "${GREEN}[*] Installing Dependencies...${NC}"
if [ -f "./venv/bin/pip" ]; then
    ./venv/bin/pip install -r requirements.txt -q
else
    # Fallback for some systems where venv might be weird
    echo -e "${RED}[!] Error: pip not found in venv. Trying to fix...${NC}"
    python3 -m venv venv --without-pip
    source venv/bin/activate
    curl https://bootstrap.pypa.io/get-pip.py | python
    pip install -r requirements.txt
fi

# 5. Create Launch Shortcut
echo -e "${GREEN}[*] Creating './vortex' shortcut...${NC}"
cat <<EOF > vortex
#!/bin/bash
cd "\$(dirname "\$0")"
./venv/bin/python3 main.py "\$@"
EOF
chmod +x vortex

echo -e "\n${BLUE}=======================================${NC}"
echo -e "${GREEN}[+] OPEN SOURCE READY! INSTALLATION COMPLETE${NC}"
echo -e "${BLUE}=======================================${NC}"
echo -e "To use the tool, simply run:"
echo -e "    ${GREEN}./vortex${NC}          (Interactive Mode)"
echo -e "    ${GREEN}./vortex <target>${NC} (Direct Mode)"
