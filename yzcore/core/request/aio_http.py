#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml, lxm, zq
@date: 2020-10-23
@desc: ...

        # 当返回的 Json 串不是一个标准的 Json 时，
        # resp.json() 函数可以传递一个函数对 json 进行预处理，
        # 如：resp.json(replace(a, b))，replace()函数表示 a 替换为 b。

        # aiohttp 使用 response.read() 函数处理字节流，使用 with open() 方式保存文件或者图片
        # response.read() 函数可以传递数字参数用于读取多少个字节，如：response.read(3)读取前 3 个字节。

参考：https://github.com/raphaelauv/fastAPI-aiohttp-example
"""
import asyncio
from socket import AF_INET
from typing import TypeVar, Union, Optional, List, Dict, AnyStr

try:
    import json as _json
except (ImportError, ModuleNotFoundError):
    import json as _json

try:
    import aiohttp
    from pydantic import BaseModel, Field
except (ImportError, ModuleNotFoundError):

    AioHttpParams = List[Dict[str, Union[str, int, Dict[str, Union[str, int]]]]]
else:
    class AioHttpParams(BaseModel):
        method: AnyStr
        url: AnyStr
        params: Optional[Dict]
        data: Optional[Dict]
        json_: Optional[Dict] = Field(alias='json')
        headers: Optional[Dict]
        timeout: Optional[int]


RequestParams = TypeVar("RequestParams", bound=AioHttpParams)

SIZE_POOL_AIOHTTP = 100
CONCURRENCY = 100  # 限制并发量为1024


class AioHTTP:
    """
    注意：
    在FastAPI中使用时，在事件处理的勾子中全局设置 AioHTTP 的开启和关闭：
    app = FastAPI(
            on_startup=[AioHTTP.on_startup],
            on_shutdown=[AioHTTP.on_shutdown]
        )
    """
    semaphore: asyncio.Semaphore = asyncio.Semaphore(CONCURRENCY)
    session: aiohttp.ClientSession = None

    # def __init__(self, cookies=None, json_serialize=_json.dumps):
    #     self.session = aiohttp.ClientSession(
    #         cookies=cookies,
    #         json_serialize=json_serialize
    #     )

    @classmethod
    def get_session(cls, cookies=None,
                    json_serialize=_json.dumps) -> aiohttp.ClientSession:
        if cls.session is None or cls.session.closed:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                family=AF_INET,
                limit_per_host=SIZE_POOL_AIOHTTP
            )
            cls.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                cookies=cookies,
                json_serialize=json_serialize,
            )
        return cls.session

    @classmethod
    async def get(cls, url, params=None, data=None,
                  json=None, headers=None, timeout=30, **kwargs):
        """异步GET请求"""
        return await cls.fetch(
            'get', url, params, data, json, headers, timeout, **kwargs)

    @classmethod
    async def post(cls, url, params=None, data=None,
                   json=None, headers=None, timeout=30, **kwargs):
        """异步POST请求"""
        return await cls.fetch(
            'post', url, params, data, json, headers, timeout, **kwargs)

    @classmethod
    async def put(cls, url, params=None, data=None,
                  json=None, headers=None, timeout=30, **kwargs):
        """异步PUT请求"""
        return await cls.fetch(
            'put', url, params, data, json, headers, timeout, **kwargs)

    @classmethod
    async def patch(cls, url, params=None, data=None,
                    json=None, headers=None, timeout=30, **kwargs):
        """异步PATCH请求"""
        return await cls.fetch(
            'patch', url, params, data, json, headers, timeout, **kwargs)

    @classmethod
    async def delete(cls, url, params=None, data=None,
                     json=None, headers=None, timeout=30, **kwargs):
        """异步DELETE请求"""
        return await cls.fetch(
            'delete', url, params, data, json, headers, timeout, **kwargs)

    @classmethod
    async def fetch(
            cls, method: str, url: str,
            params=None, data=None,
            json=None, headers=None, timeout=30, **kwargs
    ):
        """
        公共请求调用方法

        :param method:  请求方法
        :param url:     请求路由
        :param params:  请求参数
        :param data:    请求的Form表单参数
        :param json:    请求的Json参数
        :param headers: 请求头参数
        :param timeout: 超时时间
        :return:
        """
        client_session = cls.get_session()
        __request = getattr(client_session, method.lower())
        async with cls.semaphore:
            try:
                async with __request(
                        url,
                        params=params,
                        data=data,
                        json=json,
                        headers=headers,
                        timeout=timeout,
                        **kwargs
                ) as response:
                    result = await response.json()
                # await cls.session.close()
            except Exception as e:
                import traceback
                traceback.print_exc()
                return {'detail': e}, 500
            else:
                return result, response.status

    @classmethod
    async def bulk_request(cls, querys: List[RequestParams]):
        """
        异步批量请求

        :param querys:
        [
            {'method': 'get', 'url': 'http://httpbin.org/get', 'params': {'key': 'value{}'.format(1)}},
            {'method': 'get', 'url': 'http://httpbin.org/get', 'params': {'key': 'value{}'.format(2)}},
            {'method': 'get', 'url': 'http://httpbin.org/get', 'params': {'key': 'value{}'.format(3)}},
            {'method': 'get', 'url': 'http://httpbin.org/get', 'params': {'key': 'value{}'.format(4)}},
            {'method': 'get', 'url': 'http://httpbin.org/get', 'params': {'key': 'value{}'.format(5)}},
            {'method': 'post', 'url': 'http://httpbin.org/post', 'json': {'key': 'value{}'.format(6)}},
            {'method': 'post', 'url': 'http://httpbin.org/post', 'json': {'key': 'value{}'.format(7)}},
            {'method': 'post', 'url': 'http://httpbin.org/post', 'json': {'key': 'value{}'.format(8)}},
            {'method': 'post', 'url': 'http://httpbin.org/post', 'json': {'key': 'value{}'.format(9)}},
            {'method': 'post', 'url': 'http://httpbin.org/post', 'json': {'key': 'value{}'.format(10)}},
        ]

        :return:
        """
        tasks = [asyncio.ensure_future(cls.fetch(**kw)) for kw in querys]
        responses = await asyncio.gather(*tasks)
        return responses

    @classmethod
    async def close(cls):
        if cls.session:
            await cls.session.close()

    @classmethod
    async def on_startup(cls):
        cls.get_session()

    @classmethod
    async def on_shutdown(cls):
        await cls.close()



