#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
from fastapi import APIRouter,HTTPException
from fastapi import Query,Body
from yzcore.core.response import response
from yzcore.logger import get_logger
from yzcore.exceptions import CreateObjectFailed, UpdateObjectFailed
from .schemas import PermissionBase


logger = get_logger(__name__)
logger.debug('test_debug')


router = APIRouter()


@router.get('/resources/{resource_id}')
def view_get_info(resource_id: int):
    """
    GET 示例

        :param resource_id:
        :return:
    """
    raise HTTPException(status_code=404, detail='找不到对象')


@router.get('/resources/')
def view_list_resources(
        query: str = Query('keyword'),
        limit: int = Query(10, gt=0, le=1000),
        offset: int = Query(0, ge=0),
):
    """
    GET 列表查询示例

        :param query:
        :param limit:
        :param offset:
        :return:
    """


@router.post("/resources/")
def view_create_resources(
        body: PermissionBase
):
    """
    POST 示例

        :param body:
        :return:
    """
    raise CreateObjectFailed()


@router.put("/resources/{resource_id}")
def view_update_resources(
        resource_id: int,
        body: PermissionBase
):
    """
    PUT 全量更新示例

        :param body:
        :return:
    """
    raise UpdateObjectFailed()


@router.patch("/resources/{resource_id}")
def view_update_resources(
        resource_id: int,
        body: PermissionBase
):
    """
    PATCH 局部更新示例

        :param body:
        :return:
    """
    raise UpdateObjectFailed()