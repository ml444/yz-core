#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021-1-22
@desc: 通过函数调用uuid-service服务
"""
from yzcore.default_settings import default_setting as settings
from yzcore.request import request

__all__ = [
    "generate_uuid",
    "explain_uuid",
    "translate2timestamp",
    "make_uuid",
]


if settings.ID_URL is None:
    raise EnvironmentError("Error: 'ID_URL' is None.")


def generate_uuid(limit: int = 1) -> int or list:
    """
    根据参数生成一定数量的ID

    :param limit:
    :return:
            1: 6918460366603157505
            2: [6918460407405346817, 6918460407405347841,...]
    """
    url = f"{settings.ID_URL}{settings.GENERATE_UUID_PATH}"
    result, status_code = request(
        'get', url, params={'limit': limit}
    )
    if status_code == 200:
        if limit == 1:
            return int(result['id'])
        else:
            return [int(_id) for _id in result['id_list']]


def explain_uuid(long_id: int) -> dict:
    """
    解析长整型ID为 id_object

    :param long_id: 6918460366603157505
    :return: {
              "machine_id": 1,
              "sequence": 0,
              "time_duration": 867377,
              "generate_method": 2,
              "mode_type": 1,
              "version": 0
            }
    """
    url = f"{settings.ID_URL}{settings.EXPLAIN_UUID_PATH}"
    result, status_code = request(
        'get', url, params={'long_id': long_id}
    )
    if status_code == 200:
        return result


def translate2timestamp(time_duration: int):
    """
    把时间间隔转换为时间戳

    :param time_duration: 时间间隔
    :return: {
               "timestamp": 1611219039,
               "datetime": "2021-01-21T16:50:39"
             }
    """
    url = f"{settings.ID_URL}{settings.TRANSLATE_PATH}"
    result, status_code = request(
        'get', url, params={'time_duration': time_duration})
    if status_code == 200:
        return result


def make_uuid(sequence: int, timestamp: int,
            machine: int=None, method: int=None,
            mtype: int=None, version: int=None
):
    """
    根据传入参数合成长整型id

    :param sequence:
    :param timestamp:
    :param machine:
    :param method:
    :param mtype:
    :param version:
    :return:
    """
    data = {
        "sequence": sequence,
        "timestamp": timestamp,
        "machine": machine,
        "method": method,
        "mtype": mtype,
        "version": version
    }
    data = {k: v for k, v in data.items() if v is not None}
    url = f"{settings.ID_URL}{settings.MAKE_UUID_PATH}"
    result, status_code = request('post', url, json=data)
    if status_code == 200:
        return int(result['id'])


