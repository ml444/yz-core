#!/usr/bin/python3.6+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-13
@desc: ...
"""
import os

try:
    import yaml
except:
    yaml = None

from pydantic import BaseSettings
from yzcore.utils import get_random_secret_key


class DefaultSetting(BaseSettings):
    class Config:
        case_sensitive = False  # 是否区分大小写

    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = get_random_secret_key()

    DB_URI: str


def get_settings():
    try:
        from ..settings import Settings
    except:
        Settings = DefaultSetting

    settings = Settings()
    return settings


def get_configer(ext: str = "ini", import_path=os.curdir):
    profile = os.environ.get('ENV_PROFILE', 'dev')
    if profile == 'production':
        configname = 'config_production'
    elif profile == 'testing':
        configname = 'config_testing'
    else:
        configname = 'config_dev'
    print(f"===>当前环境为：{profile}!导入的配置文件为：{configname}.{ext}")

    base_path = os.path.abspath(import_path)
    _path = os.path.join(base_path, "conf", f"{configname}.{ext}")
    print(_path)
    if ext in ["ini", "cfg"]:
        import configparser
        conf = configparser.ConfigParser()
        conf.read(_path)
    elif ext in ["yaml", "yml"]:
        assert yaml is not None, "Need to install PyYaml"
        conf = yaml.safe_load(open(_path))
    else:
        raise AttributeError(f"暂不支持该文件格式: {ext}")
    return conf


def get_ini_section_to_dict(
        section: str,
        exclude: set = None,
        conf_parser=None
):
    """
    获取ini配置文件某个节选的全部数据，转换成字典

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


if __name__ == '__main__':
    conf = get_configer("ini")