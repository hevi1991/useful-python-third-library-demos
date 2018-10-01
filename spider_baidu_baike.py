#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import ssl

"""
使用BeautifulSoup进行爬百度百科的词条链接
"""

base_url = "https://baike.baidu.com"
his = ["/item/%E7%BC%96%E7%A8%8B"]

for i in range(20):
    url = base_url + his[-1]

    context = ssl._create_unverified_context()
    html = urlopen(url, context=context).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')

    print(i+1, soup.find('h1').get_text(), 'url: ', url)

    # find valid urls
    sub_urls = soup.find_all('a', {'target': '_blank', 'href': re.compile('/item/(%.{2})+$')})

    if len(sub_urls) != 0:
        next_url = random.sample(sub_urls, 1)[0]['href']
        his.append(next_url)
    else:
        # no valid sub link found
        his.pop()
