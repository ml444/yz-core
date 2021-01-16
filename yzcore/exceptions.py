#!/usr/bin/python3.6+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-8-5
@desc: 全局异常类定义
"""
from typing import Any

from fastapi import HTTPException


class NotFoundObject(HTTPException):
    def __init__(self, detail: Any = 'Not Found', headers: dict = None):
        super().__init__(status_code=404, detail=detail, headers=headers)


class MultiObjects(HTTPException):
    def __init__(self, detail: Any = '', headers: dict = None):
        detail = '{}存在多个对象，不符合唯一性要求'.format(detail)
        super().__init__(status_code=500, detail=detail, headers=headers)


class CreateObjectFailed(HTTPException):
    def __init__(self, detail: Any = 'Object create failed', headers: dict = None):
        super().__init__(status_code=400, detail=detail, headers=headers)


class UpdateObjectFailed(HTTPException):
    def __init__(self, detail: Any = 'Object update failed', headers: dict = None):
        super().__init__(status_code=400, detail=detail, headers=headers)


class NoObjectCreated(HTTPException):
    def __init__(self, detail: Any = 'No object was created', headers: dict = None):
        super().__init__(status_code=400, detail=detail, headers=headers)


class AlreadyExistObject(HTTPException):
    def __init__(self, detail: Any = 'Already Exist', headers: dict = None):
        super().__init__(status_code=400, detail=detail, headers=headers)


class RequestParamsError(HTTPException):
    def __init__(self, detail: Any = 'Incorrect request parameters', headers: dict = None):
        super().__init__(status_code=400, detail=detail, headers=headers)


class RequestParamsMissing(HTTPException):
    def __init__(self, detail: Any = 'Missing request parameters', headers: dict = None):
        super().__init__(status_code=400, detail=detail, headers=headers)


class NoPermission(HTTPException):
    def __init__(self, detail: Any = 'Insufficient permissions', headers: dict = None):
        super().__init__(status_code=401, detail=detail, headers=headers)


class UnknownError(HTTPException):
    def __init__(self, detail: Any = 'Unknown error', headers: dict = None):
        super().__init__(status_code=500, detail=detail, headers=headers)


if __name__ == '__main__':
    pass