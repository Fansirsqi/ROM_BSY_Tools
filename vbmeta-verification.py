#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   vbmeta-verification.py
@Time    :   2024/10/12 11:30:41
@Author  :   Byseven
@Version :   1.0
@Github  :   https://www.github.com/Fansirsqi
@Desc    :   用于处理 vbmeta.img 的校验功能
"""

import argparse
from io import BufferedRandom

# 定义魔数和标志位的常量
AVB_MAGIC = b'AVB0'
AVB_MAGIC_LEN = 4
FLAGS_OFFSET = 123
FLAG_ENABLE = b'\x00'
FLAG_DISABLE = b'\x02'


def disable_verify(f: BufferedRandom) -> None:
    """禁用 vbmeta.img 的校验功能"""
    f.seek(FLAGS_OFFSET)
    before_flag_value = f.read(1)
    if before_flag_value == FLAG_DISABLE:
        print('The vbmeta image is already disabled.')
        return
    else:
        f.seek(FLAGS_OFFSET)
        f.write(FLAG_DISABLE)
    print(f'Successfully disabled verification on the provided vbmeta image. {before_flag_value} ==> {FLAG_DISABLE}')


def enable_verify(f: BufferedRandom) -> None:
    """启用 vbmeta.img 的校验功能"""
    f.seek(FLAGS_OFFSET)
    before_flag_value = f.read(1)
    if before_flag_value == FLAG_ENABLE:
        print('The vbmeta image is already enabled.')
        return
    else:
        f.seek(FLAGS_OFFSET)
        f.write(FLAG_ENABLE)
    print(f'Successfully enabled verification on the provided vbmeta image. {before_flag_value} ==> {FLAG_ENABLE}')


def main():
    parser = argparse.ArgumentParser(description='Disable or enable vbmeta verification.')
    parser.add_argument('vbmeta_image', help='Path to the vbmeta image. / vbmeta.img 的路径')
    parser.add_argument('--disable', action='store_true', help='Disable verity and verification in vbmeta. / 去除 vb 验证')
    parser.add_argument('--enable', action='store_true', help='Enable verity and verification in vbmeta. / 恢复 vb 验证')
    args = parser.parse_args()

    # 读取 vbmeta 文件并执行启用或禁用操作
    try:
        vbmeta_image_path = args.vbmeta_image
        with open(vbmeta_image_path, 'r+b') as f:
            # 检查魔数以确认是有效的 vbmeta 文件
            magic = f.read(AVB_MAGIC_LEN)
            if magic != AVB_MAGIC:
                print('Error: The provided image is not a valid vbmeta image.')
                return
            # 根据命令行参数执行对应操作
            if args.disable:
                disable_verify(f)
            elif args.enable:
                enable_verify(f)
            else:
                print('Please specify --disable or --enable.')
    except Exception as e:
        print(f'Error: Failed when processing the vbmeta image - {str(e)}')


if __name__ == '__main__':
    main()
