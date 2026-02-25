import requests
import socket

# Link chứa danh sách Domain của bạn
SOURCE_URL = "https://raw.githubusercontent.com"

def get_ip(domain):
    try:
        # Thực hiện phân giải tên miền sang IP
        return socket.gethostbyname(domain.strip())
    except:
        return None

def main():
    try:
        print(f"Đang tải danh sách domain từ {SOURCE_URL}...")
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        
        domains = [line.strip() for line in response.text.splitlines() if line.strip()]
        ip_list = []

        print(f"Đang phân giải {len(domains)} tên miền...")
        for domain in domains:
            ip = get_ip(domain)
            if ip:
                ip_list.append(ip)
                print(f"Thành công: {domain} -> {ip}")
            else:
                print(f"Thất bại: Không thể tìm IP cho {domain}")

        # Loại bỏ các IP trùng lặp
        unique_ips = sorted(list(set(ip_list)))

        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in unique_ips:
                f.write(f"{ip}\n")
        
        print(f"Hoàn thành! Đã lưu {len(unique_ips)} IP vào dns_VN.txt")
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")
        exit(1)

if __name__ == "__main__":
    main()
