import json
from pydantic import BaseModel
from typing import Any


class Setting(BaseModel):
    banner_path: str = './banners/00'
    'banner路径'
    version: str = 'v1.0.0'
    '版本'
    version_desc: str = 'Alpha Edition'
    '版本描述'

    class Config:
        # 允许设置字段名不区分大小写
        # allow_population_by_field_name = True
        populate_by_name = True

    def save(self, file_path: str) -> None:
        """将设置保存到文件"""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.model_dump(), file, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, file_path: str) -> 'Setting':
        """从文件加载设置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return cls(**data)
        except FileNotFoundError:
            # 文件不存在时，返回默认设置
            return cls()

    def add(self, file_path: str, **kwargs: Any) -> None:
        """更新设置并保存到文件"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save_to_file(file_path)


# # 示例用法
# file_path = 'settings.json'

# # 初始化设置
# setting = Setting()

# # 修改并保存设置
# setting.update_and_save(file_path, version='v1.0.1', is_show_banner=False)

# # 从文件中加载设置
# loaded_setting = Setting.load_from_file(file_path)
# print(Setting.banner_path)
