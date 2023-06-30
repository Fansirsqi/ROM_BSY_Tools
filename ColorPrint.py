import os

class ColorPrint:
    COLORS = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37'
    }

    @staticmethod
    def print(text='', color=None, font_weight="bold", end='\n'):
        STYLES = {
            'normal': '0',
            'bold': '1',
            'italic': '3',
            'underline': '4',
            'strikethrough': '9'
        }
        if color and color.lower() in ColorPrint.COLORS:
            color_code = ColorPrint.COLORS[color.lower()]
            text = '\033[{};{}m{}\033[0m'.format(color_code, STYLES[font_weight], text)
        print(text, end=end)

