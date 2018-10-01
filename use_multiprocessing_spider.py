#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用beautifulsoup和requests, 用分布式爬取莫烦python的所有网页链接
"""

import multiprocessing as mp
import time

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://morvanzhou.github.io"

def crawl(url):
    """
    获取html文本
    :param url: 连接地址
    :return: html文本
    """
    fake_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    response = requests.get(url, headers=fake_headers)
    return response.text


def parse(html):
    """
    解析html得到需要的结果
    :param html: html文本
    :return: list 包含标题, 页面包含的链接, 抓取的页面
    """
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {'href': re.compile('^/.+?/$')})
    title = soup.find('title').get_text().strip()
    page_urls = set([BASE_URL + url['href'] for url in urls])
    url = soup.find('meta', {'property': 'og:url'})['content']
    return title, page_urls, url


def normal_way():
    """
    单线程爬虫
    :return:
    """
    unseen = {BASE_URL}
    seen = set()

    count, t1 = 1, time.time()

    while len(unseen) != 0:

        print('\nDistributed Crawling...')
        htmls = [crawl(url) for url in unseen]

        print('\nDistributed Parsing...')
        results = [parse(html) for html in htmls]

        print('\nAnalysing...')
        seen.update(unseen)  # seen the crawled
        unseen.clear()  # nothing unseen

        for title, page_urls, url in results:
            print(count, title, url)
            count += 1
            unseen.update(page_urls - seen)  # get new url to crawl

    print('Total time: %.1f s' % (time.time() - t1,))

def multiprocessing_way():
    """
    分布式爬虫
    :return:
    """
    unseen = {BASE_URL}
    seen = set()
    pool = mp.Pool()

    count, t1 = 1, time.time()
    while len(unseen) != 0:

        print('\nDistributed Crawling...')
        crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
        htmls = [j.get() for j in crawl_jobs]  # request connection

        print('\nDistributed Parsing...')
        parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
        results = [j.get() for j in parse_jobs]  # parse html

        print('\nAnalysing...')
        seen.update(unseen)  # seen the crawled
        unseen.clear()  # nothing unseen

        for title, page_urls, url in results:
            print(count, title, url)
            count += 1
            unseen.update(page_urls - seen)  # get new url to crawl
    print('Total time: %.1f s' % (time.time() - t1,))



if __name__ == '__main__':
    # normal_way()
    multiprocessing_way()