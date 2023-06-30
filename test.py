# 测试img 转换~
import sys,os
sys.path.append(os.getcwd())
from utils import img2simg

proj_dir = './miui_GINKGO_V12.5.5.0.RCOCNXM_e8efe0e9bf_11.0/'
img2simg(f'{proj_dir}system.img',f'{proj_dir}system.raw.img')