# Address-Formation-through-AmAP


## Project Introduction

The aim of this project is to transform the coarse unformatted address input by the users (missing key information such as province, region) into formatted address with a precision of 6 decimal places of latitude and longitude, and extract the address information that cannot be recognized by AmAP.

## Principles

### Geocoding is a way to transfer address into latitude and longitude. 

version3:
```bash
    https://lbs.amap.com/api/webservice/guide/api-advanced/search
```
version3_2:
```bash
    https://lbs.amap.com/api/webservice/guide/api/georegeo
```
version5:
```bash
    https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch
```

Regeocoding is a way to transfer latitude and longitude back to address.
```bash
    https://lbs.amap.com/api/webservice/guide/api/georegeo
```



## Installment

### Please initial by the following steps:

1. Clone project：

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Special Requires：
   
    VPN to AmAP(Chinese spot)
  

3. Key Application:

    Users should log in AmAP and require their own key in order to have the authority to use AmAP functions such as Geocoding and Regeocoding.

    Log in url:

    ```bash
    https://lbs.amap.com
    ```

    Key application can be reached through console after log in.

    Every account can apply for 5 keys. Every key only permits 100 accurate map geocoding. More details can be seen on:

    ```bash
    https://console.amap.com/dev/flow/manage
    ```

5. Add Key to .py and run

    Users can also rename .xlsx profiles.

## Profiles Introduction

- gaode.py

  Core codes. Aims to format address through the following step: geocode address - regeocode - certification.

  Three methods of geocoding are included, and more details are compared in 'Formation Address Methods Comparing.pdf '

    - def get_location_info_v3
    ```bash
    https://restapi.amap.com/v3/place/text?keywords={province + origin_address}&city=shanghai&offset=1&page=1&key={key}
    ```

    - def get_location_info_v3_2
    ```bash
    https://restapi.amap.com/v3/geocode/geo?address={province + origin_address}&output=json&key={key}
    ```

    - def get_location_info_v5
    ```bash
    https://restapi.amap.com/v5/place/text?keywords={origin_address}&types=190402&region={province}&key={key}
    ```
    
- gaode_key.py

    Every account can apply for 5 keys. Every key only permits 100 accurate map geocoding. So this profiles allow users to change their keys while running.

- uniform.py
  
    Combine duplicate address

- catagory.py

    Divide address into correct address which can be recognize easily by v3_2 and incorrect address which should be put into v3 to be further recognized.

- .xlsx

    All .xlsx are test examples.




