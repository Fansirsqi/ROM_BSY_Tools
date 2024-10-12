import concurrent.futures
import glob
import json
import os
import platform
import subprocess
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from Log import Log
import brotli
from Cprint import _print
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn
from tqdm import tqdm
import asyncio
from one_word import get_word
from setting import Setting

config = Setting()


def read_file_to_dict(file_path, *tag) -> dict:
    """读取本地文件转换为可操作的字典

    Args:
        file_path (str): 文件路径

    Returns:
        _type_: _description_
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = eval(f.read())
        Log.success(f'✨ 配置文件 {file_path} 读取成功')
        sleep(0.1)
        return data
    except Exception as e:
        t = trans_str(tag)
        Log.error(f'[{t}] 读取错误: {e}')
        Log.error(f'请确认文件： {file_path} 是否存在？？')
        sleep(0.1)
        exit()


def write_dict_to_file(file_path, _data, _mode: str = 'w', _encoding: str = 'utf-8', *tag):
    """将数据写入文件

    Args:
        file_path (_type_): 文件名_\n
        _data (_type_): 数据内容_\n
        _mode (str): _with open mode_\n
        _encoding (str): _encoding_
    """
    try:
        with open(f'{file_path}', mode=_mode, encoding=_encoding) as write_f:
            # print(_data)
            # _data = json.loads(_data)
            write_f.write(json.dumps(_data, indent=4, ensure_ascii=False))
            write_f.close()
        Log.success(f'✨ 配置文件 {file_path} 写入成功')
        sleep(0.1)
    except Exception as e:
        t = trans_str(tag)
        Log.error(f'🔴 [{t}]写入错误: {e}')
        Log.error(f'🔴 请确认文件: {file_path} 是否存在??')
        sleep(0.1)
        exit()


def trans_str(_str):
    result = str(_str).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace('"', '').replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\r', '\r')
    sleep(0.02)
    return result


def this_path() -> str:
    """
    返回文件所在路径
    @return:
    """
    return os.path.dirname(os.path.abspath(__file__))


def show_banner():
    """打印标题"""
    try:
        with open(f'{config.banner_path}', mode='r', encoding='utf-8') as b:
            _print(b.read(), color='green')
            category = 'a'
            quote = asyncio.run(get_word(category))  # 使用 asyncio.run 调用异步方法

            print('{:>45}'.format(''), end='')
            _print(f'{config.version_desc} {config.version}', bgcolor='blue', color='white', font_weight='bold')
            _print(quote, color='yellow', font_weight='bold italic')
    except FileNotFoundError:
        _print('Banner 文件未找到', color='red')


class DotDict(dict):
    """将字典数据转换成类的形式，数据可以通过.xx的形式访问

    Args:
        dict (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        return value


def get_project_list(exclude_folders=[]):
    """获取文件夹"""
    try:
        PDIR = './Projects/'
        target_folders: list = os.listdir(PDIR)
        os.makedirs(PDIR, exist_ok=True)
        projects = []
        Log.debug(f'获取项目列表: {PDIR}')
        for id, name in enumerate(target_folders, start=1):
            if (os.path.isdir(PDIR + name)) and name not in exclude_folders:
                Log.debug(f'     {id}. {name}')
                projects.append(PDIR + name)
        return projects
    except Exception as e:
        _print(f'获取项目列表失败: {e}', color='red')


def list_zip_files():
    """列出zip文件"""
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 构建要匹配的文件路径模式
    file_pattern = os.path.join(current_dir, '*.zip')
    # 使用glob模块获取匹配的文件列表
    zip_files = glob.glob(file_pattern)
    # 打印文件列表
    count = 1
    for file in zip_files:
        file_name = file.split('\\').pop()
        _print(f'     {count}.{file_name}', color='magenta')
        print()
    return zip_files


def unzip_file(zip_path, extract_path=None):
    """解压zip文件并显示进度条

    Args:
        zip_path (str): ZIP文件路径
        extract_path (str, optional): 解压后的目标文件夹路径. 默认使用ZIP文件名作为解压文件夹名.
    """
    file_name = os.path.basename(zip_path)  # 获取文件名

    # 如果未指定解压文件夹路径，则默认使用压缩文件名作为文件夹名
    if extract_path is None:
        extract_path = os.getcwd() + './Projects/' + file_name.replace('.zip', '')

    # 创建目标文件夹（如果不存在）
    os.makedirs(extract_path, exist_ok=True)

    # 打开ZIP文件
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()  # 缓存文件列表
            file_count = len(file_list)  # 获取zip文件中的文件数量
            Log.debug('file_count', file_count)

            # 设置进度条
            with Progress(
                TextColumn('[progress.description]{task.description}'),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f'[cyan][覆盖]正在解压 {file_name}...', total=file_count)

                # 解压每个文件
                for file in file_list:
                    zip_ref.extract(file, extract_path)
                    progress.update(task, advance=1)  # 更新进度条

        print(f'{file_name} 解压完成!')

    except zipfile.BadZipFile:
        print(f'错误: {file_name} 不是有效的ZIP文件')
    except Exception as e:
        print(f'解压失败: {e}')


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
