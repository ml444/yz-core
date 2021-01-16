#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth:
@date: 2020-9-13
@desc: ...
"""
import os
import configparser
from pydantic import Field
from yzcore.default_settings import DefaultSetting

conf = configparser.ConfigParser()
base_path = os.path.dirname(__file__)
profile = os.environ.get('ENV_PROFILE', 'dev')
print(f"当前环境为：{profile}")
if profile == 'production':
    configname = 'config_production.ini'
elif profile == 'testing':
    configname = 'config_testing.ini'
else:
    configname = 'config.ini'
print(f"===>导入的配置文件为：{configname}")
path = os.path.join(base_path, "conf", configname)
print(path)
conf.read(path)


def get_conf_section_dict(
        section: str,
        exclude: set = None,
        conf_parser: configparser.ConfigParser = conf
):
    """
    获取配置文件某个节选的全部数据，转换成字典

    :param section: 节选名称
    :param exclude: 排除的字段
    :param conf_parser: 配置解析器
    :return:
    """
    conf_dict = dict()
    for k in conf_parser.options(section):
        if exclude and k in exclude:
            break
        conf_dict[k] = conf.get(section, k)
    return conf_dict


class Settings(DefaultSetting):
    PROJECT_NAME: str = 'Base'
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "{}"
    BASE_URL: str = "http://127.0.0.1:8000"

    # postgres数据库的URI
    DB_URI: str = Field(None, env="BOX_DB_URI")


settings = Settings()
