import requests
import socket
import re

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def clean_domain(text):
    # Loại bỏ khoảng trắng, protocol, và phần sau dấu gạch chéo
    text = text.strip().lower()
    text = re.sub(r'^https?://', '', text)
    text = text.split('/')[0]
    return text

def get_all_ips(domain):
    ips = set()
    try:
        # Lấy tất cả các bản ghi IPv4 (AF_INET)
        results = socket.getaddrinfo(domain, 80, socket.AF_INET)
        for item in results:
            ips.add(item[4][0]) # Trích xuất địa chỉ IP
    except Exception as e:
        print(f"Lỗi phân giải {domain}: {e}")
    return list(ips)

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        raw_lines = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
        
        ip_map = {}
        print(f"Tìm thấy {len(raw_lines)} domain. Đang xử lý...")

        for line in raw_lines:
            domain = clean_domain(line)
            if not domain: continue
            
            found_ips = get_all_ips(domain)
            for ip in found_ips:
                if ip in ip_map:
                    if domain not in ip_map[ip]:
                        ip_map[ip] += f", {domain}"
                else:
                    ip_map[ip] = domain
                print(f"Thành công: {domain} -> {ip}")

        if not ip_map:
            print("CẢNH BÁO: Không tìm thấy IP nào!")
            return

        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in sorted(ip_map.keys()):
                f.write(f"{ip} # {ip_map[ip]}\n")
        
        print(f"Hoàn thành! Đã lưu {len(ip_map)} IP vào dns_VN.txt")

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
