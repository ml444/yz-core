#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-27
@desc: 全局常量
"""
from enum import Enum


class ObjectType(Enum):
    ORGANIZ = 1
    PROJECT = 2
    SCENE = 3
    ASSETS = 4


class PermissionType(Enum):
    OWNER = 15
    ADMIN = 7
    EDITOR = 3
    VIEWER = 1
