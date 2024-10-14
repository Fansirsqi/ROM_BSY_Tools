import concurrent.futures
import glob
import json
import os
import platform
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from Log import Log
import brotli
from Cprint import _print
from tqdm import tqdm
import asyncio
from one_word import get_word
from setting import Setting
import fnmatch

config = Setting()


def comming_soon(*tag):
    "施工中"
    try:
        if tag:
            raise NotImplementedError(f'{tag}🚧  施工中')
        raise NotImplementedError('🚧  施工中')
    except Exception as e:
        _print(f'发生错误: {e}', color='red')


def trans_str(_str):
    result = str(_str).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace('"', '').replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\r', '\r')
    sleep(0.02)
    return result


def show_banner():
    """打印标题"""
    try:
        with open(f'{config.banner_path}', mode='r', encoding='utf-8') as b:
            _print(b.read(), color='green')
            category = 'a'
            quote = asyncio.run(get_word(category))  # 使用 asyncio.run 调用异步方法

            print('{:>45}'.format(''), end='')
            _print(f'{config.version_desc} {config.version}', bgcolor='blue', color='white', font_weight='bold', end='')
            print('{:<10}'.format(''))
            _print(quote, color='white', font_weight='bold italic')
    except FileNotFoundError:
        _print('Banner 文件未找到', color='red')


def get_project_list(exclude_folders=None) -> list:
    """获取项目列表"""
    if exclude_folders is None:
        exclude_folders = []

    PDIR = './Projects/'
    projects = []

    try:
        # 创建目录（如果不存在）
        os.makedirs(PDIR, exist_ok=True)
    except OSError as os_error:
        _print(f'文件操作失败: {os_error}', color='red')
        return []

    try:
        Log.debug(f'获取项目列表: {PDIR}')

        # 使用列表推导式提高效率
        projects = [os.path.join(PDIR, folder) for folder in os.listdir(PDIR) if os.path.isdir(os.path.join(PDIR, folder)) and folder not in exclude_folders]

        # 仅在有项目时打印日志
        for id, folder in enumerate(projects, start=1):
            Log.debug(f'  {id}. {folder}')

        return projects

    except Exception as e:
        _print(f'获取项目列表时发生错误: {e}', color='red')
        return []


def list_rom_files(file_types=('*.zip', '*.gz', '*.tar')):
    """列出指定后缀的文件"""
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 获取所有文件和目录
    all_files = os.listdir(current_dir)

    # 过滤匹配指定类型的文件
    zip_files = []
    for file_type in file_types:
        zip_files.extend(fnmatch.filter(all_files, file_type))

    # 打印文件列表
    if not zip_files:
        _print('未找到任何匹配的文件', color='red')
    else:
        for count, file in enumerate(zip_files, start=1):
            _print(f'  {count}. {file}', color='magenta')

    return zip_files


def clear():
    """清屏"""
    # 返回系统平台/OS的名称，如Linux，Windows，Java，Darwin
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def get_selected(text='请输选择：'):
    """获取输入信息"""
    try:
        _select = str(input(f'\033[1;33m{text}\033[0m')).strip()
        Log.debug('用户输入:', _select)
        return _select
    except KeyboardInterrupt:
        _print('输入无效，请重新输入', color='red')


def get_file_list(project_path):
    search_path = os.path.join(project_path, '*')
    # 构建要匹配的文件路径模式
    files = glob.glob(search_path)
    return files


def is_sparse_image(file_path):
    "判断是否稀疏镜像"
    # 稀疏镜像的魔术数（前4字节）
    sparse_magic = b'\x3a\xff\x26\xed'

    # 打开文件，读取前4个字节
    with open(file_path, 'rb') as f:
        file_header = f.read(4)

    # 判断文件头是否等于稀疏镜像的魔术数
    if file_header == sparse_magic:
        return True
    return False


def decompress_br_file(input_file, output_file):
    """解压br->dat"""
    try:
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                decompressor = brotli.Decompressor()
                total_size = os.path.getsize(input_file)
                file_name = output_file.split('\\')[-1]
                with tqdm(total=total_size, unit='B', desc=f'{file_name}解压中...', unit_scale=True, ncols=80) as pbar:
                    for chunk in iter(lambda: f_in.read(4096), b''):
                        decompressed_chunk = decompressor.process(chunk)
                        f_out.write(decompressed_chunk)
                        pbar.update(len(chunk))
        return f'{input_file}解压完成'
    except Exception as e:
        return f'解压出错 - {e}'


def work_job(file_list: list):
    """多线程解压br"""
    # 创建 ThreadPoolExecutor 对象池
    with ThreadPoolExecutor() as executor:
        # 提交解压任务给线程池
        futures_list = []
        for file_path in file_list:
            outfile = file_path.replace('.br', '')
            future = executor.submit(decompress_br_file, file_path, outfile)
            futures_list.append(future)
        # 获取每个任务的返回值
        for future in concurrent.futures.as_completed(futures_list):
            try:
                result = future.result()  # 获取线程的返回值
                print(f'Thread completed with result: {result}')
            except Exception as e:
                print(f'Thread raised an exception: {e}')


def dat_to_img(arguments=[]):
    subprocess.call(['./.venv/Scripts/python.exe', 'sdat2img.py'] + arguments)


def simg2img(input_file, output_file):
    """image to img"""
    _print('Starting conversion, please be patient and wait ...\n开始转换,请耐心等待...', color='yellow', end='')
    _print('[默认覆盖]', color='red')
    start_time = time.time()  # 记录开始时间
    try:
        # 调用命令行执行 img2simg.exe
        subprocess.run(['./Tool/win/simg2img.exe', input_file, output_file], check=True)
        elapsed_time = time.time() - start_time  # 计算耗时
        file = input_file.split('/')[-1]
        file2 = output_file.split('/')[-1]
        _print(f'Conversion completed successfully!\n{file} 转换 {file2}成功完成!\n耗时: {elapsed_time:.2f} 秒', color='green')
    except subprocess.CalledProcessError as e:
        _print(f'Error occurred: {e}', color='red')


def img2simg(input_file, output_file):
    """img to raw image"""
    _print('Starting conversion, please be patient and wait ...\n开始转换,请耐心等待...', color='yellow', end='')
    _print('[默认覆盖]', color='red')
    start_time = time.time()  # 记录开始时间
    try:
        # 调用命令行执行 img2simg.exe
        subprocess.run(['./Tool/win/img2simg.exe', input_file, output_file], check=True)
        elapsed_time = time.time() - start_time  # 计算耗时
        file = input_file.split('/')[-1]
        file2 = output_file.split('/')[-1]
        _print(f'Conversion completed successfully!\n{file} 转换 {file2}成功完成!\n耗时: {elapsed_time:.2f} 秒', color='green')
    except subprocess.CalledProcessError as e:
        _print(f'Error occurred: {e}', color='red')
