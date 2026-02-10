import json
from colorama import Fore, Style, init

def print_banner():
    init(autoreset=True)
    banner = f"""{Fore.RED}
    ██╗   ██╗██╗   ██╗██╗     ███╗   ██╗    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗
    ██║   ██║██║   ██║██║     ████╗  ██║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝
    ██║   ██║██║   ██║██║     ██╔██╗ ██║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ 
    ╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ 
     ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗
      ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    
    {Fore.WHITE}Advanced Bug Bounty & Reconnaissance Framework
    {Fore.YELLOW}Forged by OnlyBugs05{Style.RESET_ALL}
    """
    print(banner)

def save_report(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[-] Error saving report: {e}")
