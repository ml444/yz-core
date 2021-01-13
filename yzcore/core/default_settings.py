#!/usr/bin/python3.6+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-13
@desc: ...
"""
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
