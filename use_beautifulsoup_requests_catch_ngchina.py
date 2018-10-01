#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用beautifulsoup和requests, regex爬取国家地理的图片
"""

from bs4 import BeautifulSoup
import requests

def spider():

    URL = "http://www.ngchina.com.cn/animals/"

    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'lxml')
    img_ul = soup.find_all('ul', {'class': 'img_list'})
    for ul in img_ul:
        imgs = ul.find_all('img')
        for img in imgs:
            url = img['src']
            r = requests.get(url, stream=True)
            image_name = url.split('/')[-1]
            with open('./static/natural/%s'%image_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=512):
                    f.write(chunk)
            print('Saved %s' % image_name)

if __name__ == '__main__':
    spider()