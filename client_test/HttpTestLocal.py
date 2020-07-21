# -*- coding: utf-8 -*-

import requests


proxies = {
    'http': 'socks5://000001:Ab123145@127.0.0.1:8530'
    , 'https':'socks5://000001:Ab123145@127.0.0.1:8530'
}

url = 'https://www.baidu.com'

response = requests.get(url, proxies=proxies, timeout=120)
print(response.text)
