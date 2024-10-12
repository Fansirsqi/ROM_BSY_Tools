#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   test.py
@Time    :   2024/10/11 18:21:27
@Author  :   Byseven
@Version :   1.0
@Github  :   https://www.github.com/Fansirsqi
@Desc    :   测试文件
"""

import subprocess

'zip -r -9 update.zip META-INF/ firmware-update/ boot.img system.new.dat.br system.patch.dat system.transfer.list vendor.new.dat.br vendor.patch.dat vendor.transfer.list'


def create_flashable_package(output_file, folder_to_pack):
    """
    使用 7z 创建刷机包
    :param output_file: 生成的刷机包名称（带路径）
    :param folder_to_pack: 需要打包的文件夹路径
    :return: None
    """
    try:
        # 调用7z打包命令
        subprocess.run(['7z', 'a', '-tzip', output_file, folder_to_pack], check=True)
        print(f'Successfully created flashable package: {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error during packaging: {e}')


if __name__ == '__main__':
    # 生成的刷机包名称
    output_file = 'flashable_package.zip'
    # 需要打包的文件夹路径，比如你的META-INF、system等目录所在的文件夹
    folder_to_pack = './path_to_your_files'

    # 调用函数创建刷机包
    create_flashable_package(output_file, folder_to_pack)
