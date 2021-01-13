#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-1
@desc: ...
"""
import os


def mkdir_if_not_exist(path: str):
    """不存在就创建目录"""
    if not os.path.exists(path):
        os.makedirs(path)