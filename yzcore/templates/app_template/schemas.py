#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-10-18
@desc: ...
"""
from typing import Optional
from pydantic import BaseModel, validator


class TransformRequestBody(BaseModel):
    job_type: str
    job_uid: str
    # callback: dict
    data: Optional[dict]
    oss_conf: Optional[dict]
    # application_uid: str = '123abc'

    # @validator('callback')
    # def validate_callback(cls, value, values):
    #     """callback里面必须要有url"""
    #     if 'url' in value and value.get('url'):
    #         return value
    #     else:
    #         raise ValueError('callback里面必须要有url')