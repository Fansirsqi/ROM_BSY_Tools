import json
from pydantic import BaseModel
from typing import Any, Optional
import os


class Setting(BaseModel):
    banner_path: str = './banners/tik'
    version: str = 'v1.0.0'
    version_desc: str = 'Alpha Edition'
    config_file: str = './settings.json'
    project_path: str = './projects'

    class Config:
        extra = 'allow'


class ConfigManager:
    """配置文件的加载、保存和更新管理器"""
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.settings = None

    def load(self) -> Setting:
        """从文件加载配置或返回默认设置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.settings = Setting(**data)
                print(f"配置文件 {self.config_file} 已加载")
        else:
            self.settings = Setting()  # 使用默认配置
            print(f"配置文件 {self.config_file} 不存在，使用默认配置")
        return self.settings

    def save(self) -> None:
        """保存配置到文件"""
        if self.settings:
            with open(self.settings.config_file, 'w', encoding='utf-8') as file:
                json.dump(self.settings.model_dump(), file, ensure_ascii=False, indent=4)
            print(f"配置文件 {self.settings.config_file} 已保存")

    def add(self, **kwargs: Any) -> None:
        """更新配置并保存到文件"""
        if self.settings:
            for key, value in kwargs.items():
                setattr(self.settings, key, value)
                print(f"配置项 {key} 已更新，值为 {getattr(self.settings, key)}")
            self.save()
            self.load()

    def has(self, key: str) -> bool:
        """检查配置项是否存在"""
        if hasattr(self.settings, key) and getattr(self.settings, key) is not None:
            print(f"配置项 {key} 已存在，值为 {getattr(self.settings, key)}")
            return True
        else:
            print(f"配置项 {key} 不存在")
            return False



config_manager = ConfigManager('./settings.json')
config = config_manager.load()

# if __name__ == '__main__':
#     # 创建配置管理器并加载配置
#     config_manager = ConfigManager('./settings.json')
#     setting = config_manager.load()

#     # 检查 token 是否存在，不存在则添加
#     print(f"当前配置: {setting.model_dump()}")
#     shici_token = getattr(setting, 'shici_token', None)
#     print(config_manager.has('shici_token'),shici_token)
