from ColorPrint import *
from utils import *

class BSYTOOLS:
    def __init__(self,):
        self.tool_path = os.getcwd()
        """工具路径"""
        self.project_dir = get_folder_list(exclude_folders=['.venv','__pycache__','Tool'])
        """项目列表"""
        clear()
        self.fun1.name = '解压ROM'
        self.fun2.name = '待定'
        self.fun3.name = '待定'
        self.fun4.name = '待定'
        self.fun5.name = '待定'
        self.fun6.name = '待定'
        ColorPrint.print(self.tool_path)
        self.print_title()
        self.start()


    @staticmethod
    def fun1():
        clear()
        ColorPrint.print("fun1")
        file_list = list_zip_files()
        select = get_selected('选择你要解压的ROM:')
        file_path = file_list[int(select)-1]
        # ColorPrint.print(f'传入的文件是:{file_list[int(select)-1]}')
        unzip_file(file_path)

    @staticmethod
    def fun2():
        ColorPrint.print("fun2")

    @staticmethod
    def fun3():
        ColorPrint.print("fun3")

    @staticmethod
    def fun4():
        ColorPrint.print("fun4")

    @staticmethod
    def fun5():
        ColorPrint.print("fun5")

    @staticmethod
    def fun6():
        ColorPrint.print("fun6")

    @staticmethod
    def print_title():
        """打印标题"""
        ColorPrint.print("\033[1;31m============================================================")
        ColorPrint.print(""" ______  ____  ____  ______       _________            __   
|_   _ \|_  _||_  _.' ____ \     |  _   _  |          [  |  
  | |_) | \ \  / / | (___ \______|_/ | | \_.--.   .--. | |  
  |  __'.  \ \/ /   _.____`|______|  | | / .'`\ / .'`\ | |  
 _| |__) _ _|  |_ _| \____) |       _| |_| \__. | \__. | |  
|_______(_|______(_)\______.'      |_____|'.__.' '.__.[___] """,color="green")
        ColorPrint.print("\033[1;31m============================================================")

    def start(self):
        """开始
        """
        ColorPrint.print("=====================选择功能菜单===========================",color='cyan')
        funcdict = {
            "fun1": self.fun1,
            "fun2": self.fun2,
            "fun3": self.fun3,
            "fun4": self.fun4,
            "fun5": self.fun5,
            "fun6": self.fun6,
        }
        for i in range(len(funcdict)//2):
            print()
            if i == 0:
                a=11
                b=22
            elif i == 1:
                a=33
                b=44
            elif i == 2:
                a=55
                b=66
            ColorPrint.print('             {}.{:<20}{}.{:<20}'.format(a,list(funcdict.values())[i].name,b,list(funcdict.values())[i+1].name),color='green')
        print()
        ColorPrint.print("=====================现有项目列表===========================",color='cyan')
        print()
        f_l = get_folder_list(exclude_folders=['.venv','__pycache__','Tool'])
        # print(f'{os.getcwd()}\{f_l[0]}')
        print()
        ColorPrint.print("============================================================",color='cyan')
        try:
            fund = {
            '11':self.fun1,
            '22':self.fun2,
            '33':self.fun3,
            '44':self.fun4,
            '55':self.fun5,
            '66':self.fun6,
            }
            print()
            select = get_selected()
            if select in fund.keys():
                fund[select]()
            else:
                project_path = f'{os.getcwd()}\{self.project_dir[int(select)-1]}'
                # print(project_path)
                clear()
                files = get_file_list(project_path)
                _sysytem = check_file(files,'system.new.dat.br')
                _vendor = check_file(files,'vendor.new.dat.br')
                br_list = []
                if _sysytem:
                    br_list.append(_sysytem)
                if _vendor:
                    br_list.append(_vendor)
                else:
                    ask = get_selected('是/否 解压? 1/0:    ')
                    if ask == '1':
                        clear()
                        ColorPrint.print('开始解压',color='blue')
                        work_job(br_list)
                    elif ask == '0':
                        ColorPrint.print('不执行解压',color='magenta')
                    else:
                        ColorPrint.print('输入有误！',color='red')
                files = get_file_list(project_path)#重新获取文件列表
                _sys_dat = check_file(files,'system.new.dat')
                _ven_dat = check_file(files,'vendor.new.dat')
                _sys_trans = check_file(files,'system.transfer.list')
                _ven_trans = check_file(files,'vendor.transfer.list')
                if not _sys_trans:
                    ColorPrint.print(f'{_sys_dat}无法解压，找不到\n{_sys_trans}',color='red')
                if not _ven_trans:
                    ColorPrint.print(f'{_ven_dat}无法解压，找不到\n{_ven_trans}',color='red')
                    
                if _sys_dat:
                    _out_sys = _sys_dat.replace('new.dat','img')
                if _ven_dat:
                    _out_ven = _ven_dat.replace('new.dat','img')
                
                files = get_file_list(project_path)#重新获取文件列表
                _is_sys_img = check_file(files,'system.img')
                _is_ven_img = check_file(files,'vendor.img')
                
                if not _is_sys_img:
                    ColorPrint.print('解压system.new.dat')
                    dat_to_img([_sys_trans,_sys_dat,_out_sys])
                    ColorPrint.print('解压system.new.dat 完成',color='green')
                else:
                    ColorPrint.print('system.img 已存在-不解压')
                    
                if not _is_ven_img:
                    ColorPrint.print('解压vendor.new.dat')
                    dat_to_img([_ven_trans,_ven_dat,_out_ven])
                    ColorPrint.print('解压vendor.new.dat 完成',color='green')
                else:
                    ColorPrint.print('vendor.img 已存在-不解压')
        except Exception as e:
            ColorPrint.print(f"\n{e}\n程序被用户终止！",color='red')


BSYTOOLS()