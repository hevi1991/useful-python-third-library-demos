#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import time


async def do_network():
    async with aiohttp.ClientSession() as session:
        print('network start')
        async with session.get('http://httpbin.org/get') as resp:
            print('network end')
            with open('./static/{}.json'.format(time.time()), 'wb') as fd:
                while True:
                    chunk = await resp.content.read(512)
                    if not chunk:
                        break
                    fd.write(chunk)


tasks = [asyncio.ensure_future(do_network()) for _ in range(3)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))