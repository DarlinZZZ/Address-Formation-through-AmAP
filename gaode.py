import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import ssl


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

    def build_response(self, req, resp):
        context = create_urllib3_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.poolmanager.ssl_context = context
        return super(SSLAdapter, self).build_response(req, resp)

def check_none(input_str, default = ''):
    if input_str == None:
        return default
    else:
        return input_str

def get_location_info_v3(origin_address, province, key):

    url = f"https://restapi.amap.com/v3/place/text?keywords={province + origin_address}&city=shanghai&offset=5&page=1&key={key}"

    session = requests.Session()
    session.mount('https://', SSLAdapter())

    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        if "pois" in data and data["pois"]:
            for place in data["pois"]:
                address = check_none(place.get("address"))
                if "号" in address:
                    pname = check_none(place.get("pname"))
                    adname = check_none(place.get("adname"))
                    addname = check_none(place.get("name"))
                    name = pname + adname + address + '(' + addname + ')'
                    location = place.get("location")
                    return name, location
        else:
            return None, None
    else:
        return None, None

def get_location_info_v3_2(origin_address, province, key):
    # url = f"https://restapi.amap.com/v5/place/text?keywords={origin_address}&types=190402&region={province}&key={key}"
    url = f"https://restapi.amap.com/v3/geocode/geo?address={province + origin_address}&output=json&key={key}"

    session = requests.Session()
    session.mount('https://', SSLAdapter())

    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        if "geocodes" in data and data["geocodes"]:
            place = data["geocodes"][0]  # 取第一个结果
            # cityname = check_none(place.get("cityname"))
            # adname = check_none(place.get("adname"))
            # township = check_none(place.get("township"))
            # towncode = check_none(place.get("towncode"))
            addname = check_none(place.get("formatted_address"))

            # name = cityname + adname + addname
            name = addname
            location = place.get("location")
            return name, location
        else:
            return None, None
    else:
        return None, None

def get_location_info_v5(origin_address, province, key):
    url = f"https://restapi.amap.com/v5/place/text?keywords={origin_address}&types=190402&region={province}&key={key}"

    session = requests.Session()
    session.mount('https://', SSLAdapter())

    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        if "pois" in data and data["pois"]:
            place = data["pois"][0]  # 取第一个结果
            # cityname = check_none(place.get("cityname"))
            # adname = check_none(place.get("adname"))
            addname = check_none(place.get("name"))
            # name = cityname + adname + addname
            name = addname
            location = place.get("location")
            return name, location
        else:
            return None, None
    else:
        return None, None


def process_address(address):
    # 遇到第一个“号”时截断字符串
    if "号" in address:
        address = address.split("号")[0] + "号"
    else:
        address = address
    return address


# # 输入参数
# province = input("请输入省份: ")
# key = input("请输入API密钥: ")

province = "上海市"
key = "a387b9e1f98258a33e35398f01a19c5e"

# 读取Excel文件
df = pd.read_excel('incorrect.xlsx')

# 添加列名
if 'name' not in df.columns:
    df['name'] = None
if 'location' not in df.columns:
    df['location'] = None

# 遍历每一行，从第二行开始
for index, row in df.iterrows():
    if index < 0:  # 跳过第一行（标题）
        continue

    origin_address = row[1]  # 假设地址在第二列
    processed_address = process_address(origin_address)  # 处理地址信息
    print(processed_address)
    name, location = get_location_info_v3(processed_address, province, key)
    # name, location = get_location_info_v3_2(processed_address, province, key)
    print(name)

    df.at[index, 'name'] = name  # 假设要写入第五列，列名为'name'
    df.at[index, 'location'] = location  # 假设要写入第六列，列名为'location'

# 保存结果到新的Excel文件
df.to_excel('fix.xlsx', index=False)
