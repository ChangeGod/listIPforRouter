import requests

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def main():
    try:
        # Thêm headers để tránh bị chặn hoặc trả về rỗng
        headers = {'User-Agent': 'Mozilla/5.0'}
        print(f"Đang tải dữ liệu từ {SOURCE_URL}...")
        
        response = requests.get(SOURCE_URL, headers=headers)
        response.raise_for_status() 
        
        # Kiểm tra nội dung có thực sự tồn tại không
        content = response.text.strip()
        if not content:
            print("Cảnh báo: Dữ liệu tải về trống rỗng!")
            return

        dns_list = [line.strip() for line in content.splitlines() if line.strip()]
        
        # Ghi file (Đảm bảo tên file khớp với YAML)
        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for dns in dns_list:
                f.write(f"{dns}\n")
        
        print(f"Thành công! Đã lưu {len(dns_list)} dòng vào dns_VN.txt")
    except Exception as e:
        print(f"Lỗi: {e}")
        exit(1)

if __name__ == "__main__":
    main()
