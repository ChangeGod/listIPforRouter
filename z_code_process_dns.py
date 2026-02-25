import requests
import socket
import re
import urllib.parse

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def clean_domain(text):
    text = text.strip().lower()
    
    # Giải mã các ký tự bị mã hóa (%3A, %2F...)
    text = urllib.parse.unquote(text)
    
    # Dùng Regex để gắp chính xác tên miền
    match = re.search(r'(?:https?://)?([a-z0-9.-]+\.[a-z]{2,})', text)
    if match:
        domain = match.group(1)
        if not re.match(r'^[0-9.]+$', domain):
            return domain
    return ""

def get_ips(domain):
    ips = set()
    try:
        addr_info = socket.getaddrinfo(domain, 80, socket.AF_INET)
        for item in addr_info:
            ips.add(item[4][0])
    except Exception as e:
        # Vẫn in ra log để theo dõi nguyên nhân cụ thể
        print(f"[!] Lỗi phân giải [{domain}]: {e}")
    return ips

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        lines = [l.strip() for l in response.text.splitlines() if l.strip() and not l.startswith('#')]
        
        ip_map = {}
        failed_domains = set() # Danh sách chứa các domain không có IP
        
        print(f"Đang xử lý {len(lines)} dòng từ danh sách gốc...\n")

        for line in lines:
            domain = clean_domain(line)
            if not domain: continue
            
            found_ips = get_ips(domain)
            
            # Phân loại: Có IP thì đưa vào ip_map, Không có IP thì đưa vào failed_domains
            if not found_ips:
                failed_domains.add(domain)
            else:
                for ip in found_ips:
                    if ip in ip_map:
                        if domain not in ip_map[ip]:
                            ip_map[ip] += f", {domain}"
                    else:
                        ip_map[ip] = domain
                    print(f"[+] Thành công: {domain} -> {ip}")

        print("-" * 30)
        
        if not ip_map and not failed_domains:
            print("[-] Không có dữ liệu để xử lý. File dns_VN.txt sẽ không bị ghi đè.")
            return

        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            # 1. Ghi danh sách các IP thành công trước (đã được sắp xếp theo IP)
            for ip in sorted(ip_map.keys()):
                f.write(f"{ip} # {ip_map[ip]}\n")
            
            # 2. Ghi danh sách các domain thất bại ở cuối file (Sắp xếp theo A-Z)
            if failed_domains:
                f.write("\n# --- CÁC DOMAIN KHÔNG LẤY ĐƯỢC IP (ĐÃ CHẾT HOẶC LỖI DNS) ---\n")
                for d in sorted(failed_domains):
                    f.write(f"# {d}\n")
        
        print(f"[v] Hoàn thành! Đã lưu {len(ip_map)} IP thành công.")
        print(f"[v] Đã ghi nhận {len(failed_domains)} domain lỗi ở cuối file.")

    except Exception as e:
        print(f"[x] Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
