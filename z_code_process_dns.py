import requests

# Link Raw của file gốc (thay USER và REPO bằng tên của bạn)
SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def main():
    try:
        response = requests.get(SOURCE_URL)
        # Lấy danh sách DNS, lọc bỏ dòng trống
        dns_list = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        # Tạo file mới có tên 'dns_ket_qua.txt'
        with open("dns_ket_qua.txt", "w") as f:
            for dns in dns_list:
                f.write(f"{dns}\n")
        
        print("Đã tạo file dns_ket_qua.txt thành công!")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
