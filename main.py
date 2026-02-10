import argparse
import sys
from modules.recon import run_recon
from modules.scanner import run_scan
from modules.fuzzer import run_fuzzer
from modules.vuln_scanner import run_vuln_scan
from modules.detector import run_detector
from modules.reporter import generate_html_report
from modules.utils import print_banner, save_report
from colorama import Fore, Style, init

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="VULN-VORTEX: High-Speed Bug Bounty & Reconnaissance Framework.",
        epilog="Forged by OnlyBugs05. Happy Hunting!"
    )
    parser.add_argument("-t", "--target", help="Target domain (e.g., example.com)")
    parser.add_argument("--mode", choices=["recon", "scan", "fuzz", "vuln", "full"], default="full", help="Operation mode")
    parser.add_argument("-o", "--output", help="Output file for report (JSON)", default="report.json")
    
    args = parser.parse_args()
    
    # Interactive Mode
    if not args.target:
        print(f"{Fore.YELLOW}[?] No target provided. Entering interactive mode...{Style.RESET_ALL}\n")
        args.target = input(f"{Fore.CYAN}   > Enter Target Domain (e.g. example.com): {Style.RESET_ALL}").strip()
        if not args.target:
            print(f"{Fore.RED}[!] Target is required!{Style.RESET_ALL}")
            sys.exit(1)
            
        print(f"\n{Fore.CYAN}   Select Mode:{Style.RESET_ALL}")
        print("   1. Full Hunt (Recon + Scan + Fuzz + Vuln)")
        print("   2. Recon Only")
        print("   3. Vulnerability Scan Only")
        mode_choice = input(f"\n{Fore.CYAN}   > Enter choice [1]: {Style.RESET_ALL}").strip()
        
        if mode_choice == "2": args.mode = "recon"
        elif mode_choice == "3": args.mode = "vuln"
        else: args.mode = "full"
        print("\n")

    results = {}
    
    if args.mode in ["recon", "full"]:
        print(f"[*] Starting Reconnaissance on {args.target}...")
        results["recon"] = run_recon(args.target)
        
    # NEW Detection Step
    if args.mode in ["scan", "full"]:
        results["tech"] = run_detector(args.target) # Run detection before deep scans
    
    if args.mode in ["scan", "full"]:
        print(f"[*] Starting Security Scan on {args.target}...")
        results["scan"] = run_scan(args.target, results.get("recon", {}))

    if args.mode in ["fuzz", "full"]:
        print(f"[*] Starting Web Fuzzing on {args.target}...")
        results["fuzz"] = run_fuzzer(args.target)

    if args.mode in ["vuln", "full"]:
        print(f"[*] Starting Vulnerability Scan on {args.target}...")
        # Pass recon data if available, otherwise just target
        results["vuln"] = run_vuln_scan(args.target, results.get("recon", {}))
        
    save_report(results, args.output)
    
    # Generate HTML Report automatically
    generate_html_report(args.output, "report.html")
    print(f"\n[+] Hunt finished! JSON saved to {args.output}")
    print(f"[+] ⚡ DASHBOARD READY: Open report.html in your browser ⚡")

if __name__ == "__main__":
    main()
