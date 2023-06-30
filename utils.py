from datetime import datetime, timedelta
import json
import os
from time import sleep
import glob
import zipfile
from ColorPrint import *
from tqdm import tqdm
import platform
import subprocess
import brotli
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import time

def read_file_to_dict(file_path,*tag)-> dict:
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

def write_dict_to_file(file_path, _data, _mode:str= 'w', _encoding:str='utf-8',*tag):
    """将数据写入文件

    Args:
        file_path (_type_): 文件名_\n
        _data (_type_): 数据内容_\n
        _mode (str): _with open mode_\n
        _encoding (str): _encoding_
    """
    try:
        with open(f"{file_path}", mode=_mode, encoding=_encoding) as write_f:
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
        result = str(_str).replace('(','').replace(')','').replace(',','').replace("'",'').replace('"','').replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\r', '\r')
        sleep(0.02)
        return result

def this_path()-> str:
        """
        返回文件所在路径
        @return:
        """
        return os.path.dirname(os.path.abspath(__file__))

class Log:
    """日志打印模块，包含了一个输入获取模块，保持控制台字体一致

    Returns:
        (Any): _description_
    """
    font_yellow = '\033[1;33m'# 黄色
    font_red = '\033[1;31m' # 红色
    font_blue = '\033[1;34m' # 蓝色
    font_gray = '\033[1;30m' # 灰色
    font_green = '\033[1;32m' # 绿色
    font_purple = '\033[1;35m' # 紫色
    font_cyan = '\033[1;36m' # 青色
    font_white = '\033[1;37m' # 白色
    
    bg_red = '\033[41m' # 红色 白字
    bg_green = '\033[42m' # 绿色 深灰字
    bg_yellow = '\033[43m' # 黄色 灰字
    bg_blue = '\033[44m' # 蓝色 白字
    bg_purple = '\033[45m' #紫色 白字
    bg_cyan = '\033[46m' # 青色 深灰字
    bg_gray = '\033[47m' # 灰色 深灰字
    reset = '\033[0m'
    
    @staticmethod
    def warning(*context):
        """打印黄色警告"""
        context = trans_str(context)
        print(f'{Log.font_yellow}⚠️  [WARNING] |\n{context} {Log.reset}') 
    @staticmethod
    def error(*context):
        """打印红色错误警告"""
        context = trans_str(context)
        print(f'{Log.font_red}🔴 [ERROR]   |\n{context} {Log.reset}')
    @staticmethod
    def info(*context):
        """打印蓝色信息"""
        context = trans_str(context)
        print(f'{Log.font_blue}🔵 [INFO]    |\n{context} {Log.reset}')
    @staticmethod
    def success(*context):
        """打印绿色信息"""
        context = trans_str(context)
        print(f'{Log.font_green}🟢 [SUCCESS] |\n{context} {Log.reset}')
    @staticmethod
    def debug(*context):
        """打印灰色信息"""
        context = trans_str(context)
        print(f'{Log.font_gray}⚙️  [DEBUG]   |\n{context} {Log.reset}')
    @staticmethod
    def input(context):
        """获取输入信息"""
        data = input(f'{Log.font_white}✍️  [INPUT]   |\n{context} {Log.reset}')
        return data

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

def get_folder_list(exclude_folders=None):
    """获取文件夹"""
    folder_list = [name for name in os.listdir('.') if os.path.isdir(name) and name not in exclude_folders]
    count = 1
    for i in folder_list:
        ColorPrint.print(f'     {count}.{i}',color='blue')
        print
    return folder_list

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
        ColorPrint.print(f'     {count}.{file_name}',color='magenta')
        print()
    return zip_files

def unzip_file(zip_path, extract_path=None):
    """解压zip"""
    file_name = zip_path.split('\\').pop()
    # 如果未指定解压文件夹路径，则默认使用压缩文件名作为文件夹名
    if not extract_path:
        extract_path = os.path.splitext(zip_path)[0]  # 使用压缩文件名作为文件夹名
    # 创建目标文件夹（如果不存在）
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_count = len(zip_ref.namelist())  # 获取zip文件中的文件数量
        with tqdm(total=file_count, unit='B',desc=f'{extract_path}解压中...',ncols=80,unit_scale=True) as pbar:
            for file in zip_ref.namelist():
                zip_ref.extract(file, extract_path)
                pbar.update(1)  # 更新进度条
    ColorPrint.print(f'{file_name} 解压完成!')

def clear():
    """清屏"""
    # 返回系统平台/OS的名称，如Linux，Windows，Java，Darwin
    system = platform.system()
    if (system == u'Windows'):
        os.system('cls')
    else:
        os.system('clear')

def get_selected(text='请输选择：'):
    """获取输入信息"""
    return input(f'\033[1;33m{text}\033[0m')

def get_file_list(project_path):
    search_path = os.path.join(project_path, '*')
    # 构建要匹配的文件路径模式
    files = glob.glob(search_path)
    return files

def check_file(files:list,filter=None):
    """验证system.new.dat.br"""
    name_list=[]
    for i in files:
        file_name = i.split('\\')[-1]
        name_list.append(file_name)
    if filter in name_list:
        ColorPrint.print(f'检测到 {filter} 文件',color='magenta')
        return files[name_list.index(f'{filter}')]
    else:
        ColorPrint.print(f'{filter},文件可能不存在',color='red')
        return False

def decompress_br_file(input_file, output_file):
    """解压br->dat"""
    try:
        with open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                decompressor = brotli.Decompressor()
                total_size = os.path.getsize(input_file)
                file_name = output_file.split('\\')[-1]
                with tqdm(total=total_size, unit='B',desc=f'{file_name}解压中...', unit_scale=True, ncols=80) as pbar:
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
            outfile = file_path.replace('.br','')
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
    subprocess.call(['./.venv/Scripts/python.exe','sdat2img.py'] + arguments)

def simg2img(input_file, output_file):
    """image to img"""
    ColorPrint.print('Starting conversion, please be patient and wait ...\n开始转换,请耐心等待...',color='yellow',end='')
    ColorPrint.print('[默认覆盖]',color='red')
    start_time = time.time()  # 记录开始时间
    try:
        # 调用命令行执行 img2simg.exe
        subprocess.run(['./Tool/win/simg2img.exe', input_file, output_file], check=True)
        elapsed_time = time.time() - start_time  # 计算耗时
        file = input_file.split('/')[-1]
        file2 = output_file.split('/')[-1]
        ColorPrint.print(f'Conversion completed successfully!\n{file} 转换 {file2}成功完成!\n耗时: {elapsed_time:.2f} 秒', color='green')
    except subprocess.CalledProcessError as e:
        ColorPrint.print(f'Error occurred: {e}',color='red')
        
def img2simg(input_file, output_file):
    """img to raw image"""
    ColorPrint.print('Starting conversion, please be patient and wait ...\n开始转换,请耐心等待...',color='yellow',end='')
    ColorPrint.print('[默认覆盖]',color='red')
    start_time = time.time()  # 记录开始时间
    try:
        # 调用命令行执行 img2simg.exe
        subprocess.run(['./Tool/win/img2simg.exe', input_file, output_file], check=True)
        elapsed_time = time.time() - start_time  # 计算耗时
        file = input_file.split('/')[-1]
        file2 = output_file.split('/')[-1]
        ColorPrint.print(f'Conversion completed successfully!\n{file} 转换 {file2}成功完成!\n耗时: {elapsed_time:.2f} 秒', color='green')
    except subprocess.CalledProcessError as e:
        ColorPrint.print(f'Error occurred: {e}',color='red')
