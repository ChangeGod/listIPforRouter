import requests
import socket
import re

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def clean_domain(text):
    # Loại bỏ http:// hoặc https:// nếu có
    text = re.sub(r'^https?://', '', text)
    # Loại bỏ các đường dẫn phía sau dấu / (ví dụ: domain.com/abc -> domain.com)
    text = text.split('/')[0]
    # Loại bỏ các ký tự không phải là domain (khoảng trắng, v.v.)
    return text.strip().lower()

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Đọc từng dòng, bỏ qua dòng trống và dòng bắt đầu bằng #
        raw_lines = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
        
        ip_map = {}
        print(f"Tìm thấy {len(raw_lines)} dòng. Đang xử lý phân giải...")

        for line in raw_lines:
            domain = clean_domain(line)
            if not domain:
                continue
            try:
                # Phân giải IP
                ip = socket.gethostbyname(domain)
                
                # Lưu vào map để tránh trùng IP, gộp các domain chung IP vào chú thích
                if ip in ip_map:
                    if domain not in ip_map[ip]:
                        ip_map[ip] += f", {domain}"
                else:
                    ip_map[ip] = domain
                print(f"Thành công: {domain} -> {ip}")
            except:
                # Bỏ qua nếu không phân giải được
                continue 

        # Ghi vào file dns_VN.txt
        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in sorted(ip_map.keys()):
                f.write(f"{ip} # {ip_map[ip]}\n")
        
        print(f"Hoàn thành! Đã lưu {len(ip_map)} IP vào dns_VN.txt")

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
