#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   vbmeta-verification.py
@Time    :   2024/10/12 11:30:41
@Author  :   Byseven
@Version :   1.0
@Github  :   https://www.github.com/Fansirsqi
@Desc    :   用于处理vbmeta.img的校验功能

python script.py vbmeta.img --disable # 禁用校验
python script.py vbmeta.img --enable  # 恢复校验
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
fastboot flash vbmeta vbmeta.img
"""

import struct
import argparse

# 定义魔数和标志位的常量
AVB_MAGIC = b'AVB0'
AVB_MAGIC_LEN = 4
FLAGS_OFFSET = 123
FLAG_DISABLE_VERITY = 0x01
FLAG_DISABLE_VERIFICATION = 0x02


# 禁用校验的函数
def disable_verify(vbmeta_image_path):
    try:
        with open(vbmeta_image_path, 'r+b') as f:
            # 读取魔数（前4字节）
            magic = f.read(AVB_MAGIC_LEN)
            if magic != AVB_MAGIC:
                print('Error: The provided image is not a valid vbmeta image.')
                return

            # 定位到FLAGS_OFFSET位置并读取标志位
            f.seek(FLAGS_OFFSET)
            flags = struct.unpack('B', f.read(1))[0]

            # 修改标志位以禁用verity和verification
            flags |= FLAG_DISABLE_VERITY | FLAG_DISABLE_VERIFICATION

            # 将修改后的标志位写回FLAGS_OFFSET位置
            f.seek(FLAGS_OFFSET)
            f.write(struct.pack('B', flags))

            print('Successfully disabled verification on the provided vbmeta image.')
    except FileNotFoundError:
        print(f'Error: Unable to access the provided vbmeta image at {vbmeta_image_path}.')
    except Exception as e:
        print(f'Error: Failed when patching the vbmeta image - {str(e)}')


# 恢复校验的函数
def enable_verify(vbmeta_image_path):
    try:
        with open(vbmeta_image_path, 'r+b') as f:
            # 读取魔数（前4字节）
            magic = f.read(AVB_MAGIC_LEN)
            if magic != AVB_MAGIC:
                print('Error: The provided image is not a valid vbmeta image.')
                return

            # 定位到FLAGS_OFFSET位置并读取标志位
            f.seek(FLAGS_OFFSET)
            flags = struct.unpack('B', f.read(1))[0]

            # 移除禁用verity和verification的标志位
            flags &= ~(FLAG_DISABLE_VERITY | FLAG_DISABLE_VERIFICATION)

            # 将修改后的标志位写回FLAGS_OFFSET位置
            f.seek(FLAGS_OFFSET)
            f.write(struct.pack('B', flags))

            print('Successfully re-enabled verification on the provided vbmeta image.')
    except FileNotFoundError:
        print(f'Error: Unable to access the provided vbmeta image at {vbmeta_image_path}.')
    except Exception as e:
        print(f'Error: Failed when patching the vbmeta image - {str(e)}')


# 主函数，解析命令行参数
def main():
    parser = argparse.ArgumentParser(description='Disable or enable vbmeta verification.')
    parser.add_argument('vbmeta_image', help='Path to the vbmeta image./vbmeta.img的路径')
    parser.add_argument('--disable', action='store_true', help='Disable verity and verification in vbmeta./去除vb验证')
    parser.add_argument('--enable', action='store_true', help='Enable verity and verification in vbmeta./恢复vb验证')

    args = parser.parse_args()

    if args.disable:
        disable_verify(args.vbmeta_image)
    elif args.enable:
        enable_verify(args.vbmeta_image)
    else:
        print('Please specify --disable or --enable.')


# 程序入口
if __name__ == '__main__':
    main()
