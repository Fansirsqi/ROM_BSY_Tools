import os
from time import sleep
from Cprint import _print
from utils import clear, get_file_list, get_project_list, get_selected, list_rom_files, show_banner, comming_soon, set_terminal_title
from extract_rom import unzip_file


class BSYTOOLS:
    def __init__(self):
        self.tool_path = os.getcwd()  # 工具路径
        self.project_dir: list = get_project_list(exclude_folders=['.venv', '__pycache__', 'Tool', '.git'])  # 项目列表
        # 设置终端标题
        set_terminal_title('ROM-BSY-TOOLS')

        clear()
        self.function_names = [
            ('解压Rom', self.fun1),
            ('项目列表', self.fun2),
            ('新建项目', self.fun3),
            ('删除项目', self.fun4),
            ('设置', self.fun5),
            ('关于', self.fun6),
        ]
        self.sub_function_names = [
            ('解压br', self.sub_fun1),
            ('打包br', self.sub_fun2),
            ('解包dat', self.sub_fun3),
            ('打包dat', self.sub_fun4),
            ('解包img', self.sub_fun5),
            ('打包img', self.sub_fun6),
        ]
        _print(self.tool_path)

        self.main_menu()
        # self.show_sub_functions()

    # 定义一个装饰器
    @staticmethod
    def tips(func):
        """装饰器，用于在函数执行前显示提示信息"""

        def wrapper(*args, **kwargs):
            clear()
            _print('\n00 返回上一层\n', color='yellow', font_weight='bold')
            # 执行原始函数
            _print('\n==========请输入选择对应功能前的数字以选择对应功能==========\n', color='yellow')
            result = func(*args, **kwargs)

            return result

        return wrapper

    @staticmethod
    def show_menu_name(menu_name=None):
        """显示菜单名称"""
        if not menu_name:
            return print()
        return _print(f'  -> {menu_name}\n', color='#FF5733', bgcolor='#FFFF33')

    # 计算填充的方法
    @staticmethod
    def calculate_padding(text, total_width):
        """计算文本填充宽度"""
        try:
            from wcwidth import wcswidth  # 用于计算字符串的实际宽度
        except ImportError:
            # 调用系统pip安装
            os.system('pip install wcwidth')
            from wcwidth import wcswidth
        text_width = wcswidth(text)  # 计算文本的实际宽度
        return total_width - text_width

    @tips
    def fun1(self):
        """解压ROM"""

        while True:
            try:
                file_list = list_rom_files()

                if not file_list:
                    _print(f'\n!!未找到任何刷机包,请将刷机包移至工具[{self.tool_path}]目录后再执行此功能\n', color='red')
                    input('按任意键返回至主菜单...')
                    sleep(3)
                    return self.main_menu()  # 如果没有ZIP文件，则返回主菜单

                _print('可选择的ZIP文件:', color='cyan')
                for index, file in enumerate(file_list, start=1):
                    _print(f'{index}. {file}', color='white', font_weight='bold')

                _select = get_selected('请选择:')

                if _select == '00':  # 返回上一层
                    return self.main_menu()

                # 检查输入是否有效
                try:
                    selected_index = int(_select) - 1
                    if 0 <= selected_index < len(file_list):
                        file_path = file_list[selected_index]
                        unzip_file(file_path)
                        _print('解压完成！', color='green')
                        sleep(2)
                        return self.main_menu()  # 解压完成后返回主菜单
                    else:
                        _print('输入不合法！请重新选择:', color='red')
                        sleep(2)

                except ValueError:
                    _print('无效输入！请输入有效数字:', color='red')
                    sleep(2)

            except Exception as e:
                _print(f'发生错误: {e}', color='red')  # 捕获其他可能的异常并输出错误信息
                sleep(3)
                return self.main_menu()  # 出现异常时返回主菜单

    @tips
    def fun2(self):
        """显示项目列表"""
        try:
            self.show_menu_name('项目列表')
            _print(self.project_dir)
            _print()
            for idx, project in enumerate(self.project_dir, start=1):
                project_name = os.path.basename(project)
                _print(f'{idx:>3}. {project_name:<20}', color='#33FFFF', bgcolor=None, font_weight='blod')
                _print()

        except Exception as e:
            _print(f'发生错误: {e}')

    @tips
    def fun3(self):
        _print('待定功能3', color='yellow')

    @tips
    def fun4(self):
        _print('待定功能4', color='yellow')

    @tips
    def fun5(self):
        _print('待定功能5', color='yellow')

    @tips
    def fun6(self):
        _print('待定功能6', color='yellow')

    @tips
    def sub_fun1(self, project_dir):
        "解压br"
        comming_soon('解包br')
        files = get_file_list(project_dir)

    @tips
    def sub_fun2(self):
        "打包br"
        comming_soon('打包br')

    @tips
    def sub_fun3(self):
        "解包dat"
        comming_soon('解包dat')

    @tips
    def sub_fun4(self):
        "打包dat"
        comming_soon('打包dat')

    @tips
    def sub_fun5(self):
        "解包img"
        comming_soon('解包img')

    @tips
    def sub_fun6(self):
        "打包img"
        comming_soon('打包img')

    def show_functions(self):
        """显示功能菜单"""
        _print()
        menu_width = 30  # 总宽度，包含汉字和填充字符
        set_width = 10  # 设置索引部分的宽度

        # 定义颜色列表
        colors = [
            '#33FF57',
            '#33FFFF',
            '#3357FF',
            '#FF5733',
            '#FF9900',
            '#FF33FF',
        ]
        self.show_menu_name('功能菜单')
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

            # 计算左侧菜单的实际宽度，并生成填充
            left_part = f'{left_index:>{set_width}}. {left_name}'
            left_padding = self.calculate_padding(left_part, menu_width)

            # 打印左侧菜单项
            _print(f'{left_part}{" " * left_padding}', color=left_color, end='')

            # 如果右侧菜单存在，计算其宽度并打印
            if right_name:
                right_part = f'{right_index:>{set_width}}. {right_name}'
                right_padding = self.calculate_padding(right_part, menu_width)
                _print(f'{right_part}{" " * right_padding}\n', color=right_color)
            else:
                _print()  # 如果没有右侧菜单，则直接换行

    @tips
    def show_sub_functions(self):
        """子菜单"""
        _print()
        menu_width = 30  # 总宽度，包含汉字和填充字符
        set_width = 10  # 设置索引部分的宽度

        # 定义颜色列表
        colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']

        for idx in range(0, len(self.sub_function_names), 2):
            # 奇数项索引和功能名称
            left_index = (idx + 1) * 11
            left_name = self.sub_function_names[idx][0]
            left_color = colors[idx % len(colors)]  # 从颜色列表中循环取颜色

            # 偶数项索引和功能名称
            if idx + 1 < len(self.sub_function_names):
                right_index = (idx + 2) * 11
                right_name = self.sub_function_names[idx + 1][0]
                right_color = colors[(idx + 1) % len(colors)]  # 从颜色列表中循环取颜色
            else:
                right_index = ''
                right_name = ''
                right_color = ''  # 没有偶数项时，不使用颜色

            # 计算左侧菜单的实际宽度，并生成填充
            left_part = f'{left_index:>{set_width}}. {left_name}'
            left_padding = self.calculate_padding(left_part, menu_width)

            # 打印左侧菜单项
            _print(f'{left_part}{" " * left_padding}', color=left_color, end='')

            # 如果右侧菜单存在，计算其宽度并打印
            if right_name:
                right_part = f'{right_index:>{set_width}}. {right_name}'
                right_padding = self.calculate_padding(right_part, menu_width)
                _print(f'{right_part}{" " * right_padding}\n', color=right_color)
            else:
                _print()  # 如果没有右侧菜单，则直接换行

    def handle_fun2(self, select):
        """处理项目选择"""
        try:
            project_dir = f'{os.getcwd()}\\{self.project_dir[int(select) - 1]}'
            self.show_sub_functions()

            _print(f'项目路径: {project_dir}')
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
            self.show_functions()
            # 功能字典，映射用户输入到对应的功能函数
            func_dict = {'11': self.fun1, '22': self.fun2, '33': self.fun3, '44': self.fun4, '55': self.fun5, '66': self.fun6}
            # 获取用户输入并清理空白字符
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
