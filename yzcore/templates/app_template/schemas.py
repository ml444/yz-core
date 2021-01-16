#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: xxx
@date: 2020-10-18
@desc: ...
"""
from pydantic import BaseModel, validator, ValidationError, Field
from typing import Type, Optional, Any, List, Tuple
from yzcore import exceptions as exp


class CommonBase(BaseModel):
    class Config:
        orm_mode = True


class PermissionBase(CommonBase):
    object_id: int
    object_type: int
    parent_id: Optional[int]
    parent_type: Optional[int]

    @validator('object_type')
    def validate_object_type(cls, value, values):
        """object_type in [1,2,3,4]"""
        if value not in [1, 2]:
            raise exp.RequestParamsError('该类型不能创建权限')

        # 为后期权限颗粒度变细准备：
        if value > 2 and not all((values['parent_id'], values['parent_type'])):
            raise exp.RequestParamsError('该类型需要传入parent')
        return value
