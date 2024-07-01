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


def check_none(input_str, default=''):
    if input_str is None:
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
        return None, None
    else:
        return None, None


def process_address(address):
    if "号" in address:
        address = address.split("号")[0] + "号"
    return address


def main():
    province = "上海市"
    key = input("请输入API密钥: ")

    df = pd.read_excel('incorrect.xlsx')
    if 'name' not in df.columns:
        df['name'] = None
    if 'location' not in df.columns:
        df['location'] = None

    index = 0
    while index < len(df):
        row = df.iloc[index]

        if index == 0:
            index += 1
            continue

        origin_address = row[1]  # Assuming address is in the second column
        processed_address = process_address(origin_address)
        name, location = get_location_info_v3(processed_address, province, key)

        while name is None:  # Retry with a new key if name is empty
            print(f"未能找到地址信息: {processed_address}")
            key = input("请输入另一个API密钥: ")
            name, location = get_location_info_v3(processed_address, province, key)

        df.at[index, 'name'] = name
        df.at[index, 'location'] = location

        index += 1

    df.to_excel('fix.xlsx', index=False)


if __name__ == "__main__":
    main()
