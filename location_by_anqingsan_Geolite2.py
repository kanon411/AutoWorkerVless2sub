# # """
# # 使用 ipinfo.io 查询 IP 地址的位置信息（无需导包）
# # """
# import os
# import requests
# import re


# def get_ip_location(ip_address):
#     """
#     根据 IP 地址查询其位置信息
#     """
#     response = requests.get(f"https://ipinfo.io/{ip_address}/json")
#     data = response.json()
#     location = {
#         "ip": ip_address,
#         "country": data.get("country"),
#     }
#     return location


# # def extract_ips_from_file(file_path):
# #     """
# #     从 TXT 文件中提取 IP 地址
# #     """
# #     ip_addresses = []
# #     with open(file_path, "r", encoding='utf-8') as file:  # 指定使用 'utf-8' 编码
# #         next(file)  # 跳过标题行
# #         for line in file:
# #             ip_address = line.split(",")[0]  # IP 地址在每行的第一个位置
# #             ip_addresses.append(ip_address)

# #     return ip_addresses


# def extract_ips_from_file(file_path):
#     """
#     从 TXT 文件中提取 IP 地址
#     """
#     ip_addresses = []
#     with open(file_path, "r", encoding='utf-8') as file:  # 指定使用 'utf-8' 编码
#         for line in file:
#             match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)  # 匹配IP地址
#             if match:
#                 ip_address = match.group()  # 获取匹配的IP地址
#                 ip_addresses.append(ip_address)

#     return ip_addresses

# def main():
#     """
#     主程序入口
#     """
#     input_file_path = "ip.txt"  # 输入文件路径
#     output_file_path = "addressesapi.txt"  # 输出文件路径
#     port = 443  # 端口号

#     if not os.path.exists(input_file_path):
#         print("输入文件不存在")
#         return

#     ip_addresses = extract_ips_from_file(input_file_path)

#     with open(output_file_path, "w") as file:
#         for ip_address in ip_addresses:
#             location = get_ip_location(ip_address)
#             if location is not None:
#                 file.write(f"{location['ip']}:{port}#{location['country']}\n")
#     print('location检测完成')


# if __name__ == "__main__":
#     main()






"""
使用 GeoLite2-City.mmdb 数据库查询 IP 地址的位置信息（可用20240422）
由于改用 GeoLite2-City.mmdb 文件过大，cf无法部署，故改用 GeoLite2-Country.mmdb 文件
"""
import os
import geoip2.database
import re


def get_ip_location(ip_address):
    """
    根据 IP 地址查询其位置信息
    """
    reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
    try:
        # response = reader.city(ip_address) # 改用 GeoLite2-Country.mmdb 文件，不再返回地区信息
        response = reader.country(ip_address)

        location = {
            "ip": ip_address,
            "country": response.country.iso_code,
            # "region": response.subdivisions.most_specific.iso_code,  # 添加地区代号 改用 GeoLite2-Country.mmdb 必须注释掉，该文件中只有国家不包含地区
            # "region": response.subdivisions.most_specific.name,  # 添加地区名称 改用 GeoLite2-Country.mmdb 必须注释掉，该文件中只有国家不包含地区
        }
    except geoip2.errors.AddressNotFoundError:
        return None

    return location


# def extract_ips_from_file(file_path):
#   """
#     从 TXT 文件中提取 IP 地址
#     """
#   ip_addresses = []
#   with open(file_path, "r") as file:
#     next(file)  # 跳过标题行
#     for line in file:
#       ip_address = line.split(",")[0]  # IP 地址在每行的第一个位置
#       ip_addresses.append(ip_address)

#   return ip_addresses


def extract_ips_from_file(file_path, port_default):
    """
    从 TXT 文件中提取 IP 地址和端口号（如果存在）
    """
    ip_addresses = []
    ports = []
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            # 如果这一行以 '//' 开始，跳过这一行（相当于注释掉）
            if line.startswith('//'):
                continue

            match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if match:
                ip_address = match.group()
                port_match = re.search(r'#(\d+)', line)
                port = port_match.group(1) if port_match else port_default
                ip_addresses.append(ip_address)
                ports.append(port)

    return ip_addresses, ports


def main():
    """
    主程序入口
    """
    input_file_path = "ip.txt"  # 输入文件路径
    output_file_path = "addressesapi.txt"  # 输出文件路径
    port_default = 443  # 默认端口号

    if not os.path.exists(input_file_path):
        print("输入文件不存在")
        return

    ip_addresses, ports= extract_ips_from_file(input_file_path, port_default)

    with open(output_file_path, "w") as file:
        for ip_address in ip_addresses:
            location = get_ip_location(ip_address)
            port = ports[ip_addresses.index(ip_address)]
            
            # 如果 location 是 None，跳过这一行ip
            if location is None or location['country'] == None:
                # print('location is None')
                continue

            # file.write(f"{location['ip']}:{port}#{location['country']} {location['region']}\n")  # 国家+地区代号
            file.write(f"{location['ip']}:{port}#{location['country']}\n")  # 仅国家 
    print('location检测完成')


if __name__ == "__main__":
    main()




# # action:
# name: Run IP Location Detection

# on:
#   push:
#     paths:
#       - 'ip.txt'

# jobs:
#   build:
#     runs-on: ubuntu-latest

#     steps:
#       - name: Set up Python
#         uses: actions/setup-python@v2
#         with:
#           python-version: '3.x'

#       - name: Checkout code
#         uses: actions/checkout@v2

#       - name: Install dependencies
#         run: |
#           python -m pip install --upgrade pip
#           pip install -r requirements.txt

#       - name: Run IP Location Detection
#         run: |
#           python main.py
