from Cprint import _print
from utils import get_project_list, clear, get_selected, list_zip_files, unzip_file, get_file_list, work_job, dat_to_img, show_banner
import os


class BSYTOOLS:
    def __init__(self):
        self.tool_path = os.getcwd()  # 工具路径
        self.project_dir = get_project_list(exclude_folders=['.venv', '__pycache__', 'Tool', '.git'])  # 项目列表

        clear()
        self.function_names = [
            ('解压ROM', self.fun1),
            ('新建项目', self.fun2),
            ('删除项目', self.fun3),
            ('待定', self.fun4),
            ('待定', self.fun5),
            ('待定', self.fun6),
        ]
        _print(self.tool_path)

        self.main_menu()

    # 定义一个装饰器
    @staticmethod
    def tips(func):
        """装饰器，用于在函数执行前显示提示信息"""

        def wrapper(*args, **kwargs):
            clear()
            _print('\n00 返回上一层', color='yellow')
            _print('================================================================', color='cyan')
            # 执行原始函数
            return func(*args, **kwargs)

        return wrapper

    @tips
    def fun1(self):
        """解压ROM"""
        try:
            _print('执行功能：解压ROM', color='green')
            file_list = list_zip_files()

            if not file_list:
                _print('未找到任何ZIP文件', color='red')

            # 显示文件列表
            _print('可选择的ZIP文件:', color='cyan')
            for index, file in enumerate(file_list, start=1):
                _print(f'{index}. {file}', color='white', font_weight='bold')

            _select = get_selected('选择你要解压的ROM:')

            if _select == '00':
                self.main_menu()
            else:
                # 验证用户选择是否有效
                try:
                    selected_index = int(_select) - 1
                    if 0 <= selected_index < len(file_list):
                        file_path = file_list[selected_index]
                        unzip_file(file_path)
                    else:
                        _print('选择的索引超出范围！', color='red')
                except ValueError:
                    _print('无效选择！请选择一个有效的数字。', color='red')
        except Exception as e:
            _print(f'发生错误: {e}', color='red')  # 捕获其他可能的异常并输出错误信息

    def fun2(self):
        _print('待定功能2', color='yellow')

    def fun3(self):
        _print('待定功能3', color='yellow')

    def fun4(self):
        _print('待定功能4', color='yellow')

    def fun5(self):
        _print('待定功能5', color='yellow')

    def fun6(self):
        _print('待定功能6', color='yellow')

    def show_projects(self):
        """显示项目列表"""
        _print('=======================项目列表=============================', color='cyan')
        _print()
        for idx, project in enumerate(self.project_dir, start=1):
            project_name = os.path.basename(project)
            _print(f'{idx:^3}. {project_name:<20}', color='magenta', font_weight='blod')
            _print()

    def show_functions(self):
        """显示功能菜单"""
        _print('=======================工具选择菜单=============================', color='cyan')
        _print()

        # 定义颜色列表
        colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']

        for idx in range(0, len(self.function_names), 2):
            # 奇数项索引和功能名称
            left_index = (idx + 1) * 11
            left_name = self.function_names[idx][0]
            left_color = colors[idx % len(colors)]  # 从颜色列表中循环取颜色

            # 偶数项索引和功能名称
            if idx + 1 < len(self.function_names):
                right_index = (idx + 2) * 11
                right_name = self.function_names[idx + 1][0]
                right_color = colors[(idx + 1) % len(colors)]  # 从颜色列表中循环取颜色
            else:
                right_index = ''
                right_name = ''
                right_color = ''  # 没有偶数项时，不使用颜色

            # 打印功能项，并确保对齐
            _print(f'{left_index:>10}. {left_name:<20}', color=left_color, end='')  # 打印奇数项，不换行
            if right_name:
                _print(f'{right_index:>10}. {right_name}\n', color=right_color)  # 打印偶数项
            else:
                _print()  # 如果没有偶数项，则换行

        _print('================================================================', color='cyan')

    @tips
    def handle_project_selection(self, select):
        """处理项目选择"""
        try:
            project_path = f'{os.getcwd()}\\{self.project_dir[int(select) - 1]}'

            files = get_file_list(project_path)
            _print(f'项目路径: {project_path}')
            _print(f'文件列表: {files}')
            _select = get_selected('请选择功能或项目:').strip()
            match _select:
                case '00':
                    self.main_menu()
        except Exception as e:
            _print(f'发生错误: {e}', color='red')

    def main_menu(self):
        """开始菜单交互"""
        try:
            show_banner()
            self.show_projects()
            self.show_functions()
            # 功能字典，映射用户输入到对应的功能函数
            func_dict = {'11': self.fun1, '22': self.fun2, '33': self.fun3, '44': self.fun4, '55': self.fun5, '66': self.fun6}
            # 获取用户输入并清理空白字符
            _print('{:>10}'.format('00.退出') + '{:>10}'.format('01.设置') + '{:>10}'.format('02.下载') + '\n', color='red', font_weight='blod')
            select = get_selected('请选择功能或项目:').strip()

            match select:
                case '11' | '22' | '33' | '44' | '55' | '66':
                    func_dict[select]()  # 直接调用对应的功能函数
                case '00':
                    _print('退出程序', color='blue')
                case _:
                    _print(select)
                    self.handle_project_selection(select)
        except KeyboardInterrupt as e:
            _print(f'程序已手动退出 {e}', color='red')
        except AttributeError as e:
            _print(f'发生错误: {e}', color='red')


BSYTOOLS()
