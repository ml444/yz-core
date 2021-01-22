#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021-01-23
@desc: uid扩展模块的测试文件
"""
from tests.test_setting_reload import Settings
from yzcore.extensions import uid
LONG_ID = 2306877360852435967
TIME_DURATION = 986434592
TIME_STAMP = 1611338096592
ID_DATA = {
    'machine_id': 1023,
    'sequence': 0,
    'time_duration': 986434592,
    'generate_method': 2,
    'mode_type': 0,
    'version': 0
}


def test_generate_uuid():
    _id = uid.generate_uuid()
    assert isinstance(_id, int)
    assert len(str(_id)) == 19
    print(_id)
    global LONG_ID
    LONG_ID = _id
    _id_list = uid.generate_uuid(3)
    assert isinstance(_id_list, list)
    assert len(_id_list) == 3


def test_explain_uuid():
    id_data = uid.explain_uuid(LONG_ID)
    assert isinstance(id_data, dict)
    assert len(id_data) == 6
    assert 'time_duration' in id_data
    global TIME_DURATION, ID_DATA
    TIME_DURATION = id_data['time_duration']
    ID_DATA = id_data
    print(TIME_DURATION)
    print(id_data)


def test_translate_time():
    result = uid.translate2timestamp(TIME_DURATION)
    assert isinstance(result, dict)
    assert len(result) == 2
    global TIME_STAMP
    TIME_STAMP = result['timestamp']
    print(TIME_STAMP)


def test_make_uuid():
    data = {
        'machine': ID_DATA.get('machine_id'),
        'sequence': ID_DATA.get('sequence'),
        'timestamp': TIME_STAMP,
        'method': ID_DATA.get('generate_method'),
        'mtype': ID_DATA.get('mode_type'),
        'version': ID_DATA.get('version')
    }
    _id = uid.make_uuid(**data)
    assert isinstance(_id, int)
    assert len(str(_id)) == 19
    print(_id)
    assert _id == LONG_ID




if __name__ == '__main__':
    test_generate_uuid()
    test_explain_uuid()
    test_translate_time()
    test_make_uuid()
