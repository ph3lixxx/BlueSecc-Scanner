# BlueSecc Vulnerability Scanner 🔍

Sebuah alat pemindai kerentanan web yang mendeteksi XSS, SQL Injection, LFI, dan Open Redirect.

## Fitur ✨
- ✅ Deteksi XSS (Cross-Site Scripting)
- ✅ Deteksi SQL Injection
- ✅ Deteksi Local File Inclusion (LFI)
- ✅ Deteksi Open Redirect
- 🚀 Mode Single & Multi-Target
- 📊 Output Berwarna Interaktif

## Persyaratan 📦
- Python 3.6+
- Terminal yang mendukung ANSI colors

## Instalasi ⚙️

1. **Clone Repository**
```bash
git clone https://github.com/BlueSecc/BlueSecc-Scanner.git
cd BlueSecc-Scanner

Install Dependencies

pip install -r requirements.txt --break-system-packages

Langkah Interaktif:

Pilih mode scan:

1 Single Target (URL tunggal)

2 Multi Target (dari file .txt)

Pilih jenis scan (1-5):

Copy
1. XSS         🩸
2. SQLi        💉
3. LFI         📂
4. Open Redirect 🔀
5. Scan Semua  ☢️

Aktifkan mode verbose (y/n) untuk detail lengkap

Contoh Penggunaan:

Scan Single Target untuk XSS:

bash
Copy
[INPUT URL] http://example.com/page.php?id=1
[VERBOSE] y
Scan Multi Target untuk semua kerentanan:

bash
Copy
[FILE PATH] targets.txt
[VERBOSE] n


Contoh Output 🖥️

===========================================
  VULNERABILITY SCANNER TOOL
  By: BlueSecc
===========================================
[*] Memulai scan untuk: http://testphp.vulnweb.com/listproducts.php?cat=1
[!] Testing parameter: cat
[XSS] Potensi kerentanan ditemukan di parameter cat dengan payload: <script>alert(1)</script>
[SQLi] Potensi MySQL injection di parameter cat dengan payload: ' OR 1=1--
