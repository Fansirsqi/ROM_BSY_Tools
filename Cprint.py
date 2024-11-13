#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   Cprint.py
@Time    :   2024/10/10 11:49:03
@Author  :   Byseven
@Version :   1.0
@Github  :   https://www.github.com/Fansirsqi
@Desc    :   for Print info on screen
"""

from rich.console import Console
from rich.text import Text

console = Console()


def _print(text='', color='', bgcolor='', font_weight='', end='\n', style=None, isText=True):
    """
    自定义打印函数，支持颜色、背景颜色和样式
    如果isText=True，则text参数为Text对象,不再支持单独上色[]解析逻辑
    """
    # 确保输入是字符串类型
    try:
        if not isinstance(text, str):
            text = repr(text)
        # 生成样式字符串
        styles = [font_weight] if font_weight else []
        if color:
            styles.append(color)
        if bgcolor:
            styles.append(f'on {bgcolor}')

        _style = ' '.join(styles)  # 使用空格连接样式
        if style:
            _style = style
        if isText:
            # 创建Text对象
            text_obj = Text()
            text_obj.append(text, style=_style)  # 添加样式
        else:
            text_obj = text  # 直接打印字符串
        return console.print(text_obj, style=_style, end=end, markup=True)

    except Exception as e:
        console.print(f'错误: {e}', style='bold red')  # 错误处理


if __name__ == '__main__':
    # Call the test function
    a = _print('This is white text on blue background [blue]12.34[/blue]', color='red', bgcolor='')
