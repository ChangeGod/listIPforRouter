import requests
import socket

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def main():
    try:
        # 1. Tải danh sách domain
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Lọc bỏ dòng trống và dòng comment nếu có
        domains = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
        
        ip_results = []
        print(f"Tìm thấy {len(domains)} domain. Đang bắt đầu phân giải...")

        # 2. Chuyển domain thành IP
        for domain in domains:
            try:
                # Lấy IP (chỉ lấy IPv4)
                ip = socket.gethostbyname(domain)
                ip_results.append(ip)
                print(f"Thành công: {domain} -> {ip}")
            except Exception:
                # Bỏ qua các domain lỗi hoặc không tồn tại
                continue

        # 3. Loại bỏ trùng lặp và sắp xếp
        final_ips = sorted(list(set(ip_results)))
        
        # Ghi file
        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in final_ips:
                f.write(f"{ip}\n")
        
        print(f"Hoàn thành! Đã lưu {len(final_ips)} IP vào dns_VN.txt")

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
