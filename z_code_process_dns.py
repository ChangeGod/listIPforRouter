import socket

# Danh sách domain bạn muốn lấy IP
domains = [
    "testhethong111.com",
    "dnsleaktest.com",
    "ipleak.net",
    "tuoitre.vn"
]

def main():
    ip_list = []
    print("Đang bắt đầu phân giải IP...")
    
    for domain in domains:
        try:
            # Lấy địa chỉ IPv4 từ domain
            ip = socket.gethostbyname(domain.strip())
            ip_list.append(f"{domain}: {ip}")
            print(f"Thành công: {domain} -> {ip}")
        except socket.gaierror:
            # Trường hợp domain không tồn tại hoặc lỗi kết nối
            print(f"Lỗi: Không thể tìm thấy IP cho {domain}")
        except Exception as e:
            print(f"Lỗi không xác định với {domain}: {e}")

    # Ghi kết quả vào file dns_VN.txt
    with open("dns_VN.txt", "w", encoding="utf-8") as f:
        for entry in ip_list:
            f.write(f"{entry}\n")
    
    print(f"\nĐã lưu {len(ip_list)} địa chỉ IP vào file dns_VN.txt")

if __name__ == "__main__":
    main()
