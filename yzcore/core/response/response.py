#!/usr/bin/python3.6+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-13
@desc: ...
"""
import os
import json
import typing
from starlette.datastructures import URL
from starlette.background import BackgroundTask
from fastapi import Response as _Response
from fastapi.responses import (
    HTMLResponse, PlainTextResponse,
    JSONResponse, UJSONResponse, ORJSONResponse,
    RedirectResponse, StreamingResponse, FileResponse
)


class XMLResponse(_Response):
    media_type = "application/xml"


responses = {
    "xml": XMLResponse,
    "html": HTMLResponse,
    "plain": PlainTextResponse,
    "json": JSONResponse,
    "ujson": UJSONResponse,
    "orjson": ORJSONResponse,
    "redirect": RedirectResponse,
    "stream": StreamingResponse,
    "file": FileResponse,
}


def response(
        content: typing.Any = None,
        url: typing.Union[str, URL] = None,     # RedirectResponse 重定向使用

        path: str = None,                       # FileResponse
        filename: str = None,                   # FileResponse
        stat_result: os.stat_result = None,     # FileResponse
        method: str = None,                     # FileResponse

        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,

        mtype: str = "orjson"
):
    if 'json' in mtype:
        content = render_data(data=content)
    elif mtype in ['plain', 'xml', 'html'] and not isinstance(content, str):
        content = json.dumps(content)

    kwargs = dict(
        content=content,
        url=url,
        path=path,
        filename=filename,
        stat_result=stat_result,
        method=method,
        status_code=status_code,
        headers=headers,
        media_type=media_type,
        background=background,
    )
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    _response_cls = responses.get(mtype)
    return _response_cls(**kwargs)


def render_data(data=None, code=10000, message='Successfully.',
                limit: int = 10, offset: int = 0, total: int = 0):
    if data is None:
        return dict(
            code=code,
            message=message,
            info=dict(),
            list=dict(
                data=[],
                pagination=False
            )
        )
    if isinstance(data, list):
        result = dict(
            code=code,
            message=message,
            info=dict(),
            list=dict(
                data=data,
                pagination=dict(
                    limit=limit,
                    offset=offset,
                    total=total
                )
            )
        )
    # elif isinstance(data, Container):
    else:
        result = dict(
            code=code,
            message=message,
            info=data,
            list=dict(
                data=[],
                pagination=False
            )
        )
    return result
