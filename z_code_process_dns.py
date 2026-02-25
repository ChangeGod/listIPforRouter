import requests
import socket

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def main():
    try:
        # 1. Tải danh sách domain
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        domains = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
        
        # Sử dụng dictionary để lưu {IP: Domain} nhằm tránh trùng lặp IP nhưng vẫn giữ được chú thích
        ip_map = {}
        print(f"Tìm thấy {len(domains)} domain. Đang xử lý...")

        # 2. Chuyển domain thành IP
        for domain in domains:
            try:
                ip = socket.gethostbyname(domain)
                # Nếu IP đã tồn tại, có thể cộng dồn domain vào chú thích (tùy chọn)
                if ip in ip_map:
                    if domain not in ip_map[ip]:
                        ip_map[ip] += f", {domain}"
                else:
                    ip_map[ip] = domain
                print(f"Thành công: {domain} -> {ip}")
            except:
                continue 

        # 3. Sắp xếp và ghi file theo định dạng: IP # Domain
        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in sorted(ip_map.keys()):
                f.write(f"{ip} # {ip_map[ip]}\n")
        
        print(f"Xong! Đã lưu {len(ip_map)} IP kèm chú thích vào dns_VN.txt")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
