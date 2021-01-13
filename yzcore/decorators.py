#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-22
@desc: 权限验证的装饰器模块
"""
# from yzcore.core.request import get_request
from yzcore.exceptions import NoPermission

request = get_request()

PERMISSION_URL = 'http://localhost:9001/api/permission/'


class CheckPermission:
    def __init__(self):
        pass

    def __call__(self, func):
        def _call(permission, *args, **kw):
            print('===>decorator of class is runing')
            user_id = kw.get('user_id')
            space_id = kw.get('space_id')
            if self._validate(permission, user_id, space_id):
                return func(*args, **kw)
            else:
                raise NoPermission()
        return _call

    def _validate(self, permission, space_id, user_id):
        """"""
        # 请求参数
        data = dict(
            object_id=space_id,
            object_type=1,
            space_id=space_id,
            user_id=user_id
        )
        # 发送请求验证
        url = PERMISSION_URL
        response, status = request.get(url, json=data)
        # 判断结果
        if status == 200:
            _permission = response.get('permission')
            if permission >= _permission:
                return True
        return False


if __name__ == '__main__':
    pass
# class Bar:
#     @Foo()
#     def bar(self):
#         print('==>exec(bar)')
