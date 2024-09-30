# 使用在线网站检测ip和域名
import requests
import re
import time

def get_ip_location(ip_or_domain):
    """
    使用ip-api.com API查询IP地址或域名的位置信息
    """
    # url = f"https://ip-api.io/api/json/{ip_or_domain}"
    url = f"http://ip-api.com/json/{ip_or_domain}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            location = {
                "ip_or_domain": ip_or_domain,
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "countryCode": data.get("countryCode"),
            }
            print(f"IP或域名: {location['ip_or_domain']}, 地区: {location['countryCode']} {location['region']} {location['city']}")
            return location
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None

def extract_ips_and_domains_from_file(file_path, port_default):
    """
    从 TXT 文件中提取 IP 地址、域名和端口号（如果存在）
    """
    ip_addresses_or_domains = []
    ports = []
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            # 如果这一行以 '//' 开始，跳过这一行（相当于注释掉）
            if line.startswith('//'):
                continue

            ip_address_or_domain = None  # 设置默认值

            match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if match:
                ip_address_or_domain = match.group()
            else:
                # 如果没有找到 IP 地址，尝试查找域名
                match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
                if match:
                    ip_address_or_domain = match.group()

            if ip_address_or_domain:  # 只有当找到 IP 地址或域名时才处理
                port_match = re.search(r'#(\d+)', line)
                port = port_match.group(1) if port_match else port_default
                ip_addresses_or_domains.append(ip_address_or_domain)
                ports.append(port)

    return ip_addresses_or_domains, ports

def main():
    """
    主程序入口
    """
    input_file_path = "ip.txt"  # 输入文件路径
    output_file_path = "addressesapi.txt"  # 输出文件路径
    port_default = 443  # 默认端口号

    ip_addresses_or_domains, ports = extract_ips_and_domains_from_file(input_file_path, port_default)

    # 使用 'w' 模式打开文件，每次运行都会覆盖原文件
    with open(output_file_path, "w", encoding='utf-8') as file:
        for i, ip_address_or_domain in enumerate(ip_addresses_or_domains):
            if i != 0 and i % 45 == 0:
                print("达到45个IP检测数量，等待60秒后继续检测...")
                time.sleep(60)  # 暂停60秒

            location = get_ip_location(ip_address_or_domain)
            port = ports[ip_addresses_or_domains.index(ip_address_or_domain)]

            # 如果 location 是 None，跳过这一行ip
            if location is None or location['country'] is None:
                continue

            file.write(f"{location['ip_or_domain']}:{port}#{location['countryCode']} {location['region']}\n")

    print('location检测完成')

if __name__ == "__main__":
    main()



# 使用在线网站检测ip，不能检测域名
# import requests
# import re
# def get_ip_location(ip_address):
#     """
#     使用ip-api.com API查询IP地址的位置信息
#     """
#     url = f"http://ip-api.com/json/{ip_address}"

#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             location = {
#                 "ip": data.get("query"),
#                 "country": data.get("country"),
#                 "region": data.get("regionName"),
#                 "city": data.get("city"),
#                 "countryCode": data.get("countryCode"),
#             }
#             print(f"IP: {location['ip']}, 地区: {location['countryCode']} {location['region']} {location['city']}")
#             return location
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

#     return None

# def extract_ips_from_file(file_path, port_default):
#     """
#     从 TXT 文件中提取 IP 地址和端口号（如果存在）
#     """
#     ip_addresses = []
#     ports = []
#     with open(file_path, "r", encoding='utf-8') as file:
#         for line in file:
#             # 如果这一行以 '//' 开始，跳过这一行（相当于注释掉）
#             if line.startswith('//'):
#                 continue

#             match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
#             if match:
#                 ip_address = match.group()
#                 port_match = re.search(r'#(\d+)', line)
#                 port = port_match.group(1) if port_match else port_default
#                 ip_addresses.append(ip_address)
#                 ports.append(port)

#     return ip_addresses, ports

# def main():
#     """
#     主程序入口
#     """
#     input_file_path = "ip.txt"  # 输入文件路径
#     output_file_path = "addressesapi.txt"  # 输出文件路径
#     port_default = 443  # 默认端口号

#     ip_addresses, ports = extract_ips_from_file(input_file_path, port_default)

#     # 使用 'w' 模式打开文件，每次运行都会覆盖原文件
#     with open(output_file_path, "w", encoding='utf-8') as file:
#         for ip_address in ip_addresses:
#             location = get_ip_location(ip_address)
#             port = ports[ip_addresses.index(ip_address)]

#             # 如果 location 是 None，跳过这一行ip
#             if location is None or location['country'] is None:
#                 continue

#             file.write(f"{location['ip']}:{port}#{location['countryCode']} {location['region']}\n")

#     print('location检测完成')

# if __name__ == "__main__":
#     main()


