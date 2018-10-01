#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用requests, 爬取图片到本地
"""

import re
import requests

def main_code(from_page=1, to_page=1):
    if from_page > to_page:
        return
    url = "https://www.pexels.com/?dark=true&page={0}&format=js".format(from_page)
    fake_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    print('loading page {0}'.format(from_page))
    response = requests.get(url, headers=fake_headers)
    print('got response: ', response.text)
    with open('./static/rest.txt', 'wb') as f:
        f.write(response.content)

    rest = re.findall(r'https://[a-zA-Z0-9\-./]*\?', response.text)
    rest = list(set([x[:-1] for x in rest]))
    rest = [i for i in rest if 'users' not in i and 'photos' in i]

    for img_url in rest:
        print('start download: {0}'.format(img_url))
        img_response = requests.get(img_url, stream=True, headers=fake_headers)
        file_name = img_response.url.split('/')[-1]
        with open('./static/images/{0}'.format(file_name), 'wb') as img_f:
            for chunk in img_response.iter_content(chunk_size=512):
                img_f.write(chunk)
        print('download finish: {0}'.format(img_url))

    main_code(from_page + 1, to_page)

if __name__ == '__main__':
    start = input('请输入起始页码(默认1):')
    finish = input('请输入结束页数(默认1):')
    try:
        if start == "" and finish == "":
            main_code()
        else:
            start = int(start)
            finish = int(finish)
            main_code(start, finish)
    except ValueError as e:
        print('输入有误, 请输入整数.')



