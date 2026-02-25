import requests
import socket
import re
import urllib.parse
import time

SOURCE_URL = "https://raw.githubusercontent.com/ChangeGod/listIPforRouter/refs/heads/main/FWVietNam"

def clean_domain(text):
    """Lọc tên miền chuẩn từ các chuỗi rác, URL mã hóa (như %3A, %2F)"""
    text = text.strip().lower()
    text = urllib.parse.unquote(text)
    
    # Regex gắp chính xác tên miền, bỏ qua http, https, tham số đằng sau
    match = re.search(r'(?:https?://)?([a-z0-9.-]+\.[a-z]{2,})', text)
    if match:
        domain = match.group(1)
        # Bỏ qua nếu là IP thuần túy (chỉ chứa số và dấu chấm)
        if not re.match(r'^[0-9.]+$', domain):
            return domain
    return ""

def find_subdomains(domain):
    """Tìm các subdomain ẩn thông qua lịch sử chứng chỉ SSL (crt.sh)"""
    subdomains = {domain} # Luôn bao gồm domain gốc
    print(f"[*] Đang săn subdomain cho: {domain} ...")
    
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        # Timeout 15s để GitHub Actions không bị treo nếu crt.sh quá tải
        response = requests.get(url, headers=headers, timeout=15) 
        
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                names = entry['name_value'].lower().split('\n')
                for name in names:
                    if not name.startswith('*'): # Bỏ qua các domain dạng *.domain.com
                        subdomains.add(name)
            print(f"    -> Tìm thấy tổng cộng {len(subdomains)} biến thể.")
        else:
            print(f"    -> [!] Bỏ qua săn subdomain (Server crt.sh bận: {response.status_code})")
            
    except Exception as e:
        print(f"    -> [!] Lỗi khi truy vấn crt.sh (Có thể do timeout): {e}")
        
    return subdomains

def get_ips(domain):
    """Phân giải IP từ tên miền"""
    ips = set()
    try:
        addr_info = socket.getaddrinfo(domain, 80, socket.AF_INET)
        for item in addr_info:
            ips.add(item[4][0])
    except Exception:
        # Chúng ta pass lỗi ở đây để log không bị rác (vì sẽ có rất nhiều subdomain cũ đã chết)
        pass 
    return ips

def main():
    try:
        # 1. Tải danh sách gốc
        print("Đang tải danh sách từ GitHub...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        lines = [l.strip() for l in response.text.splitlines() if l.strip() and not l.startswith('#')]
        print(f"Đã tải {len(lines)} dòng dữ liệu.\n")
        print("-" * 30)

        # 2. Làm sạch và thu thập tất cả Domain + Subdomain
        all_targets = set()
        for line in lines:
            domain = clean_domain(line)
            if domain:
                # Tìm thêm subdomain cho mỗi domain gốc tìm được
                subs = find_subdomains(domain)
                all_targets.update(subs)
                # Nghỉ 1 giây giữa các lần gọi crt.sh để tránh bị chặn IP (Rate limit)
                time.sleep(1) 

        print("-" * 30)
        print(f"Bắt đầu phân giải IP cho {len(all_targets)} domain/subdomain...\n")

        # 3. Phân giải IP
        ip_map = {}
        success_count = 0
        
        for target in all_targets:
            found_ips = get_ips(target)
            for ip in found_ips:
                if ip in ip_map:
                    if target not in ip_map[ip]:
                        ip_map[ip] += f", {target}"
                else:
                    ip_map[ip] = target
            
            if found_ips:
                print(f"[+] Có IP: {target} -> {', '.join(found_ips)}")
                success_count += 1

        print("-" * 30)
        
        # 4. Lưu kết quả
        if not ip_map:
            print("[-] Không tìm thấy IP nào hoạt động. File dns_VN.txt giữ nguyên.")
            return

        with open("dns_VN.txt", "w", encoding="utf-8") as f:
            for ip in sorted(ip_map.keys()):
                f.write(f"{ip} # {ip_map[ip]}\n")
        
        print(f"[v] Hoàn thành! Đã tìm được IP cho {success_count} tên miền.")
        print(f"[v] Đã lưu tổng cộng {len(ip_map)} IP duy nhất vào file dns_VN.txt.")

    except Exception as e:
        print(f"[x] Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
