import pandas as pd
import re


def extract_main_info(address):
    match = re.search(r'区(.*?)号', address)
    return match.group(1) if match else None


def compare_addresses(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 替换NaN值为一个空字符串
    df = df.fillna('')

    # 创建空的数据框来存储结果
    correct_df = pd.DataFrame(columns=df.columns)
    incorrect_df = pd.DataFrame(columns=df.columns)

    # 比较第二列和第四列中的地址信息
    for index, row in df.iterrows():
        address1 = str(row[1])
        address2 = str(row[3])

        main_info1 = extract_main_info(address1)
        main_info2 = extract_main_info(address2)

        if main_info1 == main_info2:
            correct_df = correct_df.append(row)
        else:
            incorrect_df = incorrect_df.append(row)

    # 将结果写入新的Excel文件
    correct_df.to_excel('correct.xlsx', index=False)
    incorrect_df.to_excel('incorrect.xlsx', index=False)


if __name__ == "__main__":
    compare_addresses('address_test_with_results.xlsx')
