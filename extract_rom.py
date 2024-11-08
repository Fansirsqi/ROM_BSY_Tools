
import zipfile
import tarfile
import py7zr
import shutil
import os
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from py7zr import SevenZipFile, Bad7zFile

def unzip_file(file_path, extract_path=None, compression_level=5):
    """解压压缩文件并显示进度条

    Args:
        file_path (str): 压缩文件路径
        extract_path (str, optional): 解压后的目标文件夹路径. 默认使用压缩文件名作为解压文件夹名.
        compression_level (int, optional): 压缩等级 (1-9), 仅在压缩时使用. 默认为5.
    """
    # 获取文件名和后缀
    file_name = os.path.basename(file_path)
    file_extension = file_name.split('.')[-1].lower()

    # 如果未指定解压文件夹路径，则默认使用压缩文件名作为文件夹名
    if extract_path is None:
        extract_path = os.path.join(os.getcwd(), 'Projects', file_name.replace(f'.{file_extension}', ''))

    # 创建目标文件夹（如果不存在）
    os.makedirs(extract_path, exist_ok=True)

    # 根据文件类型选择解压工具
    try:
        if file_extension == 'zip':
            _unzip_zip(file_path, extract_path)
        elif file_extension in ['tar', 'gz', 'xz']:
            _unzip_tar(file_path, extract_path)
        elif file_extension == '7z':
            _unzip_7z(file_path, extract_path)
        else:
            print(f'不支持的文件格式: {file_extension}')
            return

        print(f'{file_name} 解压完成!')
    except Exception as e:
        print(f'解压失败: {e}')

def _unzip_zip(zip_path, extract_path):
    """解压ZIP文件并显示进度条"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            file_count = len(file_list)

            with Progress(
                TextColumn('[progress.description]{task.description}'),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f'[cyan][覆盖]正在解压 {os.path.basename(zip_path)}...', total=file_count)
                for file in file_list:
                    zip_ref.extract(file, extract_path)
                    progress.update(task, advance=1)
    except zipfile.BadZipFile:
        print(f'错误: {os.path.basename(zip_path)} 不是有效的ZIP文件')

def _unzip_tar(tar_path, extract_path):
    """解压TAR、GZ、XZ文件并显示进度条"""
    try:
        with tarfile.open(tar_path, 'r:*') as tar_ref:
            file_list = tar_ref.getnames()
            file_count = len(file_list)

            with Progress(
                TextColumn('[progress.description]{task.description}'),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f'[cyan][覆盖]正在解压 {os.path.basename(tar_path)}...', total=file_count)
                for file in file_list:
                    tar_ref.extract(file, extract_path)
                    progress.update(task, advance=1)
    except tarfile.TarError:
        print(f'错误: {os.path.basename(tar_path)} 不是有效的TAR文件')

def _unzip_7z(seven_zip_path, extract_path):
    """解压7Z文件并显示进度条"""
    try:
        with SevenZipFile(seven_zip_path, mode='r') as seven_zip_ref:
            file_list = seven_zip_ref.getnames()
            file_count = len(file_list)

            with Progress(
                TextColumn('[progress.description]{task.description}'),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f'[cyan][覆盖]正在解压 {os.path.basename(seven_zip_path)}...', total=file_count)
                for file in file_list:
                    seven_zip_ref.extract(extract_path, [file])
                    progress.update(task, advance=1)
    except Bad7zFile:
        print(f'错误: {os.path.basename(seven_zip_path)} 不是有效的7Z文件')

def compress_file(input_path, archive_path=None, format='zip', compression_level=5, delete_source=False):
    """
    压缩文件或文件夹，支持多种压缩格式（zip, tar, 7z），并显示进度条

    Args:
        input_path (str): 要压缩的文件或文件夹路径
        archive_path (str, optional): 压缩后的文件路径. 默认使用输入文件夹名称.
        format (str, optional): 压缩格式. 可选 'zip', 'tar', '7z'. 默认 'zip'.
        compression_level (int, optional): 压缩级别 (1-9). 默认 5.
        delete_source (bool, optional): 是否在压缩后删除源文件. 默认 False.
    """
    if archive_path is None:
        archive_path = input_path + '.' + format
    
    # 选择压缩方法
    if format == 'zip':
        _compress_zip(input_path, archive_path, compression_level)
    elif format == 'tar':
        _compress_tar(input_path, archive_path, compression_level)
    elif format == '7z':
        _compress_7z(input_path, archive_path, compression_level)
    else:
        print(f'不支持的压缩格式: {format}')
        return
    
    if delete_source:
        _delete_source(input_path)
    
    print(f'{input_path} 已压缩到 {archive_path}.')

def _compress_zip(input_path, archive_path, compression_level):
    """压缩为ZIP文件"""
    compression = zipfile.ZIP_DEFLATED if compression_level > 0 else zipfile.ZIP_STORED
    with zipfile.ZipFile(archive_path, 'w', compression=compression) as zipf:
        if os.path.isdir(input_path):
            for foldername, subfolders, filenames in os.walk(input_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zipf.write(file_path, os.path.relpath(file_path, input_path))
        else:
            zipf.write(input_path, os.path.basename(input_path))

def _compress_tar(input_path, archive_path, compression_level):
    """压缩为TAR文件（支持tar.gz, tar.xz）"""
    if archive_path.endswith('.gz'):
        mode = 'w:gz'
    elif archive_path.endswith('.xz'):
        mode = 'w:xz'
    else:
        mode = 'w'
    
    with tarfile.open(archive_path, mode) as tarf:
        if os.path.isdir(input_path):
            tarf.add(input_path, arcname=os.path.basename(input_path))
        else:
            tarf.add(input_path, arcname=os.path.basename(input_path))

def _compress_7z(input_path, archive_path, compression_level):
    """压缩为7Z文件"""
    compression_level = max(0, min(compression_level, 9))  # 7z的压缩级别范围为0-9
    with py7zr.SevenZipFile(archive_path, 'w', filters=[{'id': py7zr.FILTER_LZMA2, 'preset': compression_level}]) as archive:
        if os.path.isdir(input_path):
            archive.writeall(input_path, os.path.basename(input_path))
        else:
            archive.write(input_path, os.path.basename(input_path))

def _delete_source(input_path):
    """删除源文件或文件夹"""
    if os.path.isdir(input_path):
        shutil.rmtree(input_path)
    else:
        os.remove(input_path)



# # 压缩文件夹为zip格式，并删除源文件
# compress_file('my_folder', format='zip', compression_level=5, delete_source=True)
# # 压缩单个文件为7z格式，不删除源文件
# compress_file('example.txt', format='7z', compression_level=9, delete_source=False)
# # 压缩文件为tar.gz格式，并删除源文件
# compress_file('data_folder', format='tar', compression_level=5, delete_source=True)
# # 压缩为tar.xz格式
# compress_file('my_data', archive_path='my_data.tar.xz', format='tar', compression_level=7)

