import pandas as pd

# 读取Excel文件
df = pd.read_excel('address.xlsx')

# 提取第三列
addresses = df.iloc[:, 2]

# 定义一个函数来处理地址
def process_address(address):
    if pd.isna(address):
        return address
    if '号' in address:
        return address.split('号')[0] + '号'
    return address

# 应用函数到第三列
processed_addresses = addresses.apply(process_address)

# 将处理后的地址写入第五列（覆盖原数据）
df['第五列'] = processed_addresses

# 识别相同“路”相同“号”的地址，并统计去掉的数量
address_counts = processed_addresses.value_counts().to_dict()

# 创建字典来记录唯一地址和对应的去重数量
unique_addresses_dict = {}
for address in processed_addresses:
    if address in unique_addresses_dict:
        unique_addresses_dict[address] += 1
    else:
        unique_addresses_dict[address] = 1

# 初始化第六列和第七列的数据
unique_addresses = []
remove_counts = []

# 填充第六列和第七列的数据
for i, address in enumerate(addresses):
    processed_address = process_address(address)
    if processed_address in address_counts:
        unique_addresses.append(processed_address)
        remove_counts.append(address_counts[processed_address] - 1)
        address_counts.pop(processed_address)

# 将去重后的地址写入第六列（覆盖原数据）
df['第六列'] = [None] * len(df)
df.loc[:len(unique_addresses) - 1, '第六列'] = unique_addresses

# 将去掉的地址数量写入第七列（覆盖原数据），去掉值为0的行
df['第七列'] = [None] * len(df)
filtered_remove_counts = [count if count > 0 else None for count in remove_counts]
df.loc[:len(filtered_remove_counts) - 1, '第七列'] = filtered_remove_counts

# 保存到原来的Excel文件
df.to_excel('address.xlsx', index=False)