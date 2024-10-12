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
from setting import Setting

config = Setting()


async def get_word(category=None):
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
                sentence = '\n' + data.get('hitokoto') + '\n' + '{:>45}'.format('') + '----Re: ' + data.get('from') + '\n'
                # config.
                return sentence
            else:
                return f'Error: Received response code {response.status_code}'
        except Exception:
            return '柳色葱笼，画桡金缕，翠旗高颭香风，水光融。\n'


# 异步调用的入口函数
async def main():
    category = 'a'  # 选择动画类型
    quote = await get_word(category)
    print(f'一言: {quote}')


# 运行异步任务
if __name__ == '__main__':
    asyncio.run(main())
