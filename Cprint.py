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


def _print(text='', color=None, bgcolor=None, font_weight='normal', end='\n', **kwargs):
    """自定义打印函数，支持颜色、背景颜色和样式"""
    # 确保输入是字符串类型
    if not isinstance(text, str):
        text = repr(text)

    # 创建样式文本
    rich_text = Text(text)

    # 应用颜色和背景颜色

    if color:
        rich_text.stylize(color)
    if bgcolor:  # 只对实际内容设置背景色
        rich_text.stylize(f"on {bgcolor}")

    # 应用字体样式
    if font_weight:
        rich_text.stylize(font_weight)

    # 使用 Rich 控制台打印
    console.print(rich_text, end=end, **kwargs)


def test_print_styles():
    """Test function for printing different styles and colors, including background color."""
    test_cases = [
        {'text': 'Normal text', 'color': None, 'bgcolor': None, 'font_weight': 'normal'},
        {'text': 'Bold text', 'color': None, 'bgcolor': None, 'font_weight': 'bold'},
        {'text': 'Italic text', 'color': None, 'bgcolor': None, 'font_weight': 'italic'},
        {'text': 'Underline text', 'color': None, 'bgcolor': None, 'font_weight': 'underline'},
        {'text': 'Strikethrough text', 'color': None, 'bgcolor': None, 'font_weight': 'strikethrough'},
        {'text': 'Red bold text with yellow background', 'color': 'red', 'bgcolor': 'yellow', 'font_weight': 'bold'},
        {'text': 'Green italic text with cyan background', 'color': 'green', 'bgcolor': 'cyan', 'font_weight': 'italic'},
        {'text': 'Blue underline text with magenta background', 'color': 'blue', 'bgcolor': 'magenta', 'font_weight': 'underline'},
        {'text': 'Cyan strikethrough text with white background', 'color': 'cyan', 'bgcolor': 'white', 'font_weight': 'strikethrough'},
        {'text': 'Yellow normal text with black background', 'color': 'yellow', 'bgcolor': 'black', 'font_weight': 'normal'},
        {'text': 'Magenta bold text with green background', 'color': None, 'bgcolor': 'blue', 'font_weight': 'bold'},
    ]

    for case in test_cases:
        _print(case['text'], color=case['color'], bgcolor=case['bgcolor'], font_weight=case['font_weight'])


if __name__ == '__main__':
    # Call the test function
    test_print_styles()
    _print('This is white text on blue background', color='red', bgcolor='blue')
