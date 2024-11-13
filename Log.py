#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   Log.py
@Time    :   2024/10/10 11:45:54
@Author  :   Byseven
@Version :   1.0
@Github  :   https://www.github.com/Fansirsqi
@Desc    :   for Log
"""

# import sys
from loguru import logger
from datetime import datetime

logger.remove()
# 配置终端输出
# logger.add(sys.stdout, colorize=True, level='INFO', format='<y><b>{time:MM-DD HH:mm:ss}</b></y> <level><w>[</w>{level:^9}<w>]</w></level> | <level>{message}</level>  |  <b>{file}</b> <y>{line}</y>')
# 配置文件输出
logger.add('./logs.log', level='DEBUG', encoding='utf-8', format='{time:MM-DD HH:mm:ss} [{level}] {message} ', rotation='1 day', retention='7 days', mode='w')


class Log:
    """日志打印模块，使用loguru替代手动日志格式化"""

    @staticmethod
    def warning(*context):
        logger.warning(''.join(map(str, context)))

    @staticmethod
    def error(*context):
        logger.error(''.join(map(str, context)))

    @staticmethod
    def info(*context):
        logger.info(''.join(map(str, context)))

    @staticmethod
    def success(*context):
        logger.success(''.join(map(str, context)))

    @staticmethod
    def debug(*context):
        logger.debug(''.join(map(str, context)))

    @staticmethod
    def input(context):
        current_time = datetime.now().strftime('%m-%d %H:%M:%S')
        tag = '✍️  INPUT '
        _str = input(f'\033[1;33m{current_time}\033[0m \033[1;35m[{tag:^9}]\033[0m | \033[1;37m{context} \033[0m')
        Log.success('you entered: ', _str)
        return _str


if __name__ == '__main__':
    Log.warning('This is a warning message')
    Log.error('An error occurred!')
    Log.info('Here is some information.')
    Log.success('Operation completed successfully.')
    Log.debug('This is a debug message.')
    user_input = Log.input('Please enter your name: ')
