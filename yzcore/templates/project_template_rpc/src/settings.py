#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth:
@date: 2020-9-13
@desc: ...
"""
import os
from pydantic import Field
from yzcore.default_settings import DefaultSetting, get_configer


# yaml格式解析器
# conf = get_configer('yaml', import_path=os.path.dirname(__file__))

# ini格式解析器
conf = get_configer('ini', import_path=os.path.dirname(__file__))


class Settings(DefaultSetting):
    PROJECT_NAME: str = 'MyProject'
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "{}"
    BASE_URL: str = "http://127.0.0.1:8000"

    # postgres数据库的URI
    DB_URI: str = Field(None, env="DB_URI")
    src_path: str = os.path.abspath(os.path.dirname(__file__))  # 代码绝对路径


settings = Settings()


if __name__ == '__main__':
    conf.get('log', "name")