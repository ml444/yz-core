#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
from fastapi import APIRouter,HTTPException
from fastapi import Query,Body
from src.core.response import response
from src.core.logger import get_logger
from .schemas import TransformRequestBody
from src.core.exceptions import CreateObjectFailed

logger = get_logger(__name__)
logger.debug('test_debug')
logger.info('test_info')
logger.warn('test_warn')
logger.error('test_error')
logger.critical('test_critical')


router = APIRouter()


@router.get('/hello/')
def hello_world(query: str = Query('world')):
    """

    :param query:
    :return:
    """
    # _s = f"hello, {query}"
    # data = {'welcome': _s}
    # data = """<html><a>this is A tag</a></html>"""
    data = """<?xml version="1.0"?>
        <shampoo>
        <Header>
            Apply shampoo here.
        </Header>
        <Body>
            You'll have to use soap here.
        </Body>
        </shampoo>
        """
    return response(content=data, mtype='xml')


@router.post("/cloud/")
def test_cloud(
        job_uid: str = Query(...)
):
    """"""
    raise HTTPException(status_code=404, detail='最终啊不得')
    raise CreateObjectFailed()
    from random import choice
    results = ['SUCCESS', 'FAILURE', 'FAILURE', 'FAILURE']
    print(job_uid)
    return {'data': 'hello world', 'status': choice(results)}


# @router.post("/cloud/")
# def test_cloud(
#         body: TransformRequestBody
#         body: dict = Body()
# ):
#     """"""
#     print(body.dict())
#     return