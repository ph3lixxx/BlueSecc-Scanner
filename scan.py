import requests
import re
from urllib.parse import urlparse, parse_qs
from colorama import Fore, init
import os
import time

# Inisialisasi colorama
init(autoreset=True)

# Fungsi untuk menampilkan banner dengan efek berkedip
def show_banner():
    for _ in range(3):  # Loop untuk efek berkedip
        print(f"{Fore.BLUE}\n===========================================")
        print("               ph3lixxx                 ")
        print("===========================================")
        time.sleep(0.5)
        os.system("cls" if os.name == "nt" else "clear")  # Membersihkan layar
        time.sleep(0.2)

    print(f"{Fore.BLUE}===========================================")
    print("  VULNERABILITY SCANNER TOOL")
    print("  By: ph3lixxx")
    print("===========================================")
    print("Pilih jenis scan yang ingin dilakukan:")
    print("1. XSS (Cross-Site Scripting)")
    print("2. SQL Injection (SQLi)")
    print("3. Local File Inclusion (LFI)")
    print("4. Open Redirect")
    print("5. Scan Semua (XSS, SQLi, LFI, Open Redirect)")
    print("===========================================")

# Fungsi untuk memuat payload dari file
def load_payloads(payload_type):
    payload_file = f"payloads/{payload_type}.txt"
    if os.path.exists(payload_file):
        with open(payload_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    else:
        print(f"{Fore.RED}[!] File payload {payload_file} tidak ditemukan.")
        return []

# Fungsi utama untuk mendeteksi kerentanan
def detect_vulnerabilities(url, scan_type, verbose):
    try:
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        print(f"\n{Fore.CYAN}[*] Memulai scan untuk: {url}")
        
        for param in params:
            print(f"\n{Fore.YELLOW}[!] Testing parameter: {param}")
            
            if scan_type in ["xss", "all"]:
                xss_payloads = load_payloads("xss")
                for payload in xss_payloads:
                    test_xss(url, param, payload, verbose)
            
            if scan_type in ["sqli", "all"]:
                sqli_payloads = load_payloads("sqli")
                for payload in sqli_payloads:
                    test_sqli(url, param, payload, verbose)
            
            if scan_type in ["lfi", "all"]:
                lfi_payloads = load_payloads("lfi")
                for payload in lfi_payloads:
                    test_lfi(url, param, payload, verbose)
            
            if scan_type in ["openredirect", "all"]:
                redirect_payloads = load_payloads("openredirect")
                for payload in redirect_payloads:
                    test_open_redirect(url, param, payload, verbose)
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}")

# Fungsi untuk menguji XSS
def test_xss(url, param, payload, verbose):
    try:
        data = {param: payload}
        response = requests.get(url, params=data)
        if re.search(payload, response.text, re.IGNORECASE):
            print(f"{Fore.GREEN}[XSS] Potensi kerentanan ditemukan di parameter {param} dengan payload: {payload}")
        elif verbose:
            print(f"{Fore.RED}[XSS] Tidak rentan terhadap payload: {payload}")
    except:
        pass

# Fungsi untuk menguji SQL Injection
def test_sqli(url, param, payload, verbose):
    try:
        data = {param: payload}
        response = requests.get(url, params=data)
        errors = {
            "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*"),
            "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*"),
            "SQL Server": (r"Microsoft SQL Server", r"System.Data.SqlClient.*"),
            "Oracle": (r"ORA-[0-9]{5}", r"Oracle error")
        }
        found = False
        for db, patterns in errors.items():
            for pattern in patterns:
                if re.search(pattern, response.text):
                    print(f"{Fore.GREEN}[SQLi] Potensi {db} injection di parameter {param} dengan payload: {payload}")
                    found = True
                    break
            if found:
                break
        if verbose and not found:
            print(f"{Fore.RED}[SQLi] Tidak rentan terhadap payload: {payload}")
    except:
        pass

# Fungsi untuk menguji LFI
def test_lfi(url, param, payload, verbose):
    try:
        data = {param: payload}
        response = requests.get(url, params=data)
        if "root:" in response.text:
            print(f"{Fore.GREEN}[LFI] Potensi Local File Inclusion di parameter {param} dengan payload: {payload}")
        elif verbose:
            print(f"{Fore.RED}[LFI] Tidak rentan terhadap payload: {payload}")
    except:
        pass

# Fungsi untuk menguji Open Redirect
def test_open_redirect(url, param, payload, verbose):
    try:
        data = {param: payload}
        response = requests.get(url, params=data, allow_redirects=False)
        if 300 <= response.status_code < 400:
            location = response.headers.get('Location', '')
            if payload in location:
                print(f"{Fore.GREEN}[Open Redirect] Potensi kerentanan di parameter {param} dengan payload: {payload}")
        elif verbose:
            print(f"{Fore.RED}[Open Redirect] Tidak rentan terhadap payload: {payload}")
    except:
        pass

if __name__ == "__main__":
    show_banner()

    # Pilih mode scan
    scan_mode = input("Pilih mode scan (1: Single Target, 2: Multi Target dari file): ").strip()

    # Pilihan scan
    choice = input("Pilih jenis scan (1-5): ")

    # Opsi verbose
    verbose_choice = input("Gunakan mode verbose? (y/n): ").strip().lower()
    verbose = verbose_choice == "y"

    # Mapping pilihan ke jenis scan
    scan_options = {
        "1": "xss",
        "2": "sqli",
        "3": "lfi",
        "4": "openredirect",
        "5": "all"
    }

    # Pesan villain berdasarkan pilihan scan
    villain_quotes = {
        "1": "I prefer a real villain to a false hero.█",
        "2": "If you can't play the hero, play the villain.█",
        "3": "History will decide if I'm a villain or a hero.█",
        "4": "The villain will always be a villain if the hero tells the story...█"
    }

    if scan_mode == "1":  # Single Target
        target_url = input("Masukkan URL target (dengan parameter): ").strip()
        if choice in scan_options:
            scan_type = scan_options[choice]

            # Menampilkan pesan villain sesuai pilihan user
            if choice in villain_quotes:
                print(f"{Fore.MAGENTA}{villain_quotes[choice]}")

            detect_vulnerabilities(target_url, scan_type, verbose)
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid.")

    elif scan_mode == "2":  # Multi Target dari file
        file_path = input("Masukkan path file daftar target: ").strip()
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                urls = [line.strip() for line in file.readlines()]
                for url in urls:
                    detect_vulnerabilities(url, scan_options.get(choice, "all"), verbose)
        else:
            print(f"{Fore.RED}[!] File tidak ditemukan.")

    else:
        print(f"{Fore.RED}[!] Pilihan tidak valid.")
