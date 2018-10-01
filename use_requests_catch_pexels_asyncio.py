#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用requests, 爬取图片到本地
"""

import re
import requests
import asyncio
import aiohttp
import os

fake_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}


async def download_image(img_url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        file_name = img_url.split('/')[-1]
        print('start download: {}'.format(file_name))
        async with session.get(img_url, headers=fake_headers) as img_response:
            print('download finish: {}'.format(file_name))

            BASE_DIR = './static/images'
            if not os.path.exists(BASE_DIR):
                os.makedirs(BASE_DIR)

            with open('{0}/{1}'.format(BASE_DIR, file_name), 'wb') as fd:
                while True:
                    chunk = await img_response.content.read(512)
                    if not chunk:
                        break
                    fd.write(chunk)
                print('image {} writing finish'.format(file_name))


def main_code(looop, from_page=1, to_page=1, ):
    if from_page > to_page:
        return
    url = "https://www.pexels.com/?dark=true&page={0}&format=js".format(from_page)
    print('loading page {0}'.format(from_page))
    response = requests.get(url, headers=fake_headers)
    print('got response: ', response.text)

    rest = re.findall(r'https://[a-zA-Z0-9\-./]*\?', response.text)
    rest = list(set([x[:-1] for x in rest]))
    rest = [i for i in rest if 'users' not in i and 'photos' in i]

    tasks = [asyncio.ensure_future(download_image(img_url)) for img_url in rest]
    main_task = asyncio.wait(tasks)
    looop.run_until_complete(main_task)

    main_code(looop, from_page + 1, to_page)


if __name__ == '__main__':
    start = input('请输入起始页码(默认1):')
    finish = input('请输入结束页数(默认1):')

    loop = asyncio.get_event_loop()
    try:
        if start == "" and finish == "":
            main_code(loop)
        else:
            start = int(start)
            finish = int(finish)
            main_code(loop, start, finish)
    except ValueError as e:
        print('输入有误, 请输入整数.')
    finally:
        loop.close()
