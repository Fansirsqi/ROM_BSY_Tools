#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   one_word.py
@Time    :   2024/10/12 14:58:22
@Author  :   Byseven
@Version :   1.0
@Github  :   https://www.github.com/Fansirsqi
@Desc    :   一言api
a - 动画
b - 漫画
c - 游戏
d - 小说
e - 原创
f - 来自网络
g - 其他
"""

import httpx
import asyncio
from Log import Log
from setting import config, config_manager


async def get_word(category=None, max_length=40):
    url = 'https://v1.hitokoto.cn/'
    params = {}

    # 如果指定了分类，就添加到请求参数中
    if category:
        params['c'] = category

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                sentence = '\n' + data.get('hitokoto') + '\n' + '{:>{}}'.format('', max_length) + '----Re: ' + data.get('from') + '\n'
                # config.
                return sentence
            else:
                return f'Error: Received response code {response.status_code}'
        except Exception:
            sentence = '\n知否知否，应是绿肥红瘦\n' + '{:>{}}'.format('', max_length) + '----Re: ' + '如梦令' + '\n'
            return sentence


async def get_shici(max_length=40):
    token_url = 'https://v2.jinrishici.com/token'
    sentence_url = 'https://v2.jinrishici.com/sentence'

    async with httpx.AsyncClient() as client:
        try:
            shici_token = getattr(config, 'shici_token', '')
            while len(config.shici_token) != 32:
                response_token = await client.get(token_url)
                if response_token.status_code == 200:
                    data = response_token.json()
                    shici_token = data.get('data')
                    config_manager.add(shici_token=shici_token)
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'no-cache',
                'cookie': f'X-User-Token={config.shici_token}',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            }
            sentence_response = await client.get(sentence_url, headers=headers)
            # Log.debug(headers)
            if sentence_response.status_code == 200:
                sentence_data = sentence_response.json().get('data')

                content = f"{sentence_data.get('content')}"
                origin = sentence_data.get('origin')
                title = f"{origin.get('title')}"
                sentence = f'\n{content}\n{"":>{max_length}}[#FFD700]----Re: {title}[/#FFD700]\n'
                return sentence

        except Exception as e:
            Log.debug(e)
            sentence = '\n知否知否，应是绿肥红瘦\n' + '{:>{}}'.format('', max_length) + '[#FFD700]----Re: ' + '如梦令[/#FFD700]' + '\n'
            return sentence


# 异步调用的入口函数
async def main():
    category = 'a'  # 选择动画类型
    quote = await get_word(category)
    Log.debug(f'一言: {quote}')
    shici = await get_shici()
    Log.debug(f'诗词: {shici}')


# 运行异步任务
if __name__ == '__main__':
    asyncio.run(main())
