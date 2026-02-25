import requests
import socket
import re
import urllib.parse

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def clean_domain(text):
    text = text.strip().lower()
    
    # 1. Giải mã các ký tự bị mã hóa (%3A thành :, %2F thành /...)
    text = urllib.parse.unquote(text)
    
    # 2. Dùng Regex để "gắp" chính xác tên miền
    # Loại bỏ các tiền tố http://, https:// và các tham số nhiễu phía sau như &h=...
    match = re.search(r'(?:https?://)?([a-z0-9.-]+\.[a-z]{2,})', text)
    
    if match:
        domain = match.group(1)
        # Bỏ qua các giá trị không phải domain hợp lệ (ví dụ thuần số/IP hoặc rỗng)
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
        # Giữ lại thông báo lỗi để bạn biết domain nào thực sự "chết"
        print(f"[!] Lỗi phân giải [{domain}]: {e}")
    return ips

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        lines = [l.strip() for l in response.text.splitlines() if l.strip() and not l.startswith('#')]
        
        ip_map = {}
        print(f"Đang xử lý {len(lines)} dòng từ danh sách gốc...\n")

        for line in lines:
            # Chỉ lấy domain/subdomain có sẵn trong file, đã được làm sạch
            domain = clean_domain(line)
            if not domain: continue
            
            found_ips = get_ips(domain)
            for ip in found_ips:
                if ip in ip_map:
                    if domain not in ip_map[ip]:
                        ip_map[ip] += f", {domain}"
                else:
                    ip_map[ip] = domain
                print(f"[+] Thành công: {domain} -> {ip}")

        print("-" * 30)
        
        if not ip_map:
            print("[-] Không tìm thấy IP nào. File dns_VN.txt sẽ không bị ghi đè.")
            print('=> Nguyên nhân có thể do DNS chặn, hoặc các tên miền đã "chết".')
            return

        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in sorted(ip_map.keys()):
                f.write(f"{ip} # {ip_map[ip]}\n")
        
        print(f"[v] Hoàn thành! Đã lưu {len(ip_map)} IP vào file dns_VN.txt.")

    except Exception as e:
        print(f"[x] Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
