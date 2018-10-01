#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用requests库进行http方法请求
"""

import requests


def do_get():
    """
    get请求
    :return:
    """
    url = 'http://pythonscraping.com/pages/files/form.html'
    r = requests.get(url)
    print(r.text)


def do_post():
    """
    post请求
    :return:
    """
    url = 'http://pythonscraping.com/pages/files/processing.php'
    r = requests.post(url, data={'firstname': 'wei', 'lastname': 'he'})
    print(r.text)

def session_do_post():
    """
    使用session, 会话进行cookie的传入, 否则需要在request.get/post...方法中传入cookie
    :return: None
    """
    url = 'http://pythonscraping.com/pages/files/processing.php'
    session = requests.Session()
    r = session.post(url, data={'firstname': 'www', 'lastname': 'hhh'})
    print(r.text)

def download_file():
    """
    下载文件
    :return: None
    """
    url = 'https://morvanzhou.github.io/static/img/description/learning_step_flowchart.png'
    r = requests.get(url)
    filename = r.url.split('/')[-1]
    print('start download')
    with open('./static/{0}'.format(filename), 'wb') as f:
        f.write(r.content)
    print('download finish')

def download_big_file():
    """
    下载大文件的时候, 使用流(stream), 块(chunk)写入到本地
    :return:
    """
    url = 'https://images.pexels.com/photos/1438996/pexels-photo-1438996.jpeg'
    response = requests.get(url, stream=True)
    filename = response.url.split('/')[-1]

    print('start download')
    # content_size = int(response.headers['content-length'])
    # current_size = 0
    with open('./static/{0}'.format(filename), 'wb') as f:
        for chunk in response.iter_content(chunk_size=512):
            # current_size += len(chunk)
            # print('process: {0}%, {1}/{2}'.format(round(current_size / content_size * 100, 4), current_size, content_size))
            f.write(chunk)
    print('download finish')


if __name__ == '__main__':
    # do_get()
    # do_post()

    # session_do_post()

    # download_file()
    download_big_file()