import requests
import socket
import re

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def clean_domain(text):
    # Loại bỏ khoảng trắng 2 đầu và chuyển thành chữ thường
    text = text.strip().lower()
    
    # Nếu dòng có chứa dấu cách (ví dụ: "0.0.0.0 opstream90.com"), lấy phần tử cuối cùng
    text = text.split()[-1] 
    
    # Loại bỏ http://, https://
    text = re.sub(r'^https?://', '', text)
    
    # Loại bỏ các path phía sau (ví dụ: domain.com/path -> domain.com)
    text = text.split('/')[0]
    
    # Loại bỏ port nếu có (ví dụ: domain.com:8080 -> domain.com)
    text = text.split(':')[0]
    
    return text

def get_ips(domain):
    ips = set()
    try:
        # Lấy tất cả IPv4 của domain (đặc biệt quan trọng với Cloudflare)
        addr_info = socket.getaddrinfo(domain, 80, socket.AF_INET)
        for item in addr_info:
            ips.add(item[4][0])
    except Exception as e:
        # IN LỖI RA LOG: Giúp ta biết chính xác tại sao không tìm thấy IP
        print(f"[!] Lỗi phân giải [{domain}]: {e}")
    return ips

def main():
    try:
        # Thêm User-Agent đầy đủ hơn để tránh bị server nguồn chặn
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        lines = [l.strip() for l in response.text.splitlines() if l.strip() and not l.startswith('#')]
        
        ip_map = {}
        print(f"Đang xử lý {len(lines)} domain...\n")

        for line in lines:
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
            print("=> Nguyên nhân có thể do DNS của GitHub Actions chặn, hoặc các tên miền đã "chết".")
            return

        # Sắp xếp theo IP để file đẹp hơn
        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in sorted(ip_map.keys()):
                f.write(f"{ip} # {ip_map[ip]}\n")
        
        print(f"[v] Hoàn thành! Đã lưu {len(ip_map)} IP vào file dns_VN.txt.")

    except Exception as e:
        print(f"[x] Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
