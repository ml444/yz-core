#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""
import os
from pydantic import Field, AnyUrl
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
    DB_URI: str = Field('http://test.test.com/', env="DB_URI")
    src_path: str = os.path.abspath(os.path.dirname(__file__))  # 代码绝对路径
    ID_URL: AnyUrl = "http://127.0.0.1:8000/api/v1"


if __name__ == '__main__':
    from yzcore.default_settings import default_setting
    print(default_setting.ID_URL)
    print(default_setting.DB_URI)
