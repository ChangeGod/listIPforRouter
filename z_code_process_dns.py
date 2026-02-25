import requests
import socket

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def main():
    try:
        # 1. Tải danh sách domain
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        domains = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        ip_results = []
        print(f"Tìm thấy {len(domains)} domain. Đang lấy IP...")

        # 2. Chuyển domain thành IP
        for domain in domains:
            try:
                # Chỉ lấy IP (không kèm tên domain) để nạp vào Router
                ip = socket.gethostbyname(domain)
                ip_results.append(ip)
                print(f"OK: {domain} -> {ip}")
            except Exception:
                # Nếu domain lỗi (như testhethong111.com), bỏ qua và chạy tiếp
                print(f"Skip: {domain} không có IP")
                continue

        # 3. Lưu file (Loại bỏ các IP trùng lặp)
        final_ips = sorted(list(set(ip_results)))
        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in final_ips:
                f.write(f"{ip}\n")
        
        print(f"Hoàn thành! Đã lưu {len(final_ips)} IP vào dns_VN.txt")

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")
        # Không dùng exit(1) ở đây để GitHub Action không báo đỏ nếu chỉ là lỗi mạng nhẹ
