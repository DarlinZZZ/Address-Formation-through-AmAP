# Address-Formation-through-AmAP


# 项目名称

项目名称是一个用来展示如何编写一个完整的README文件的示例项目。这个项目包括以下内容：

- 项目简介
- 安装指南
- 使用说明
- 示例
- 贡献指南
- 许可证信息

## Project Introduction

The aim of this project is to transform the coarse unformatted address input by the users (missing key information such as province, region) into formatted address with a precision of 6 decimal places of latitude and longitude, and extract the address information that cannot be recognized by AmAP.

## Installment

请按照以下步骤进行安装：

1. 克隆本仓库：

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Special Requires：
   
- VPN to AmAP(Chinese spot)

## Profiles Introduction

- gaode.py

  Core codes. Aims to format address through the following step: geocode address - regeocode - certification.

  Three methods of geocoding are included, and the effectiveness is compared in

    ```bash
    def get_location_info_v3
    def get_location_info_v3_2
    def get_location_info_v5
    ```

  

