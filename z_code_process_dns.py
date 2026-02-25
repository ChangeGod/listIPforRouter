import requests

# Link nguồn bạn đã cung cấp
SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def main():
    try:
        print(f"Đang tải dữ liệu từ {SOURCE_URL}...")
        response = requests.get(SOURCE_URL)
        response.raise_for_status() # Kiểm tra lỗi kết nối
        
        # Lọc danh sách: bỏ khoảng trắng và dòng trống
        dns_list = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        # Lưu vào file dns_VN.txt (Khớp với lệnh git add trong YAML)
        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for dns in dns_list:
                f.write(f"{dns}\n")
        
        print(f"Thành công! Đã lưu {len(dns_list)} dòng vào dns_VN.txt")
    except Exception as e:
        print(f"Lỗi khi xử lý: {e}")
        exit(1) # Báo lỗi để GitHub Action dừng lại nếu thất bại

if __name__ == "__main__":
    main()
