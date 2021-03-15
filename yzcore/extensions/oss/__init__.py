#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021/3/8
@desc: ...

AccessKeyId         OSSAccessKeyId
file                file
key                 key
policy              policy
signature           Signature
x-obs-acl           x-oss-object-acl
x-obs-grant-read
x-obs-grant-read-acp
x-obs-grant-write-acp
x-obs-grant-full-control
x-obs-storage-class
x-obs-meta-*                                    x-oss-meta-*
x-obs-website-redirect-location
x-obs-server-side-encryption                    x-oss-server-side-encryption
x-obs-server-side-encryption-kms-key-id         x-oss-server-side-encryption-key-id
x-obs-server-side-encryption-customer-algorithm
x-obs-server-side-encryption-customer-key
x-obs-server-side-encryption-customer-key-MD5
x-obs-expires
success_action_redirect         success_action_redirect
success_action_status           success_action_status
                                x-oss-content-type
token                           x-oss-security-token
"""
import os
import json
import hmac
import urllib
import base64
import hashlib
import datetime
from importlib import import_module
from abc import ABCMeta, abstractmethod

IMAGE_FORMAT_SET = [
    'bmp', 'jpg', 'jpeg', 'png', 'tif', 'gif', 'pcx', 'tga',
    'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo',
    'eps', 'ai', 'raw', 'WMF', 'webp', 'tiff'
]


class OssManagerError(ValueError):
    """"""


class OssRequestError(Exception):
    """"""


class OssManagerBase(metaclass=ABCMeta):
    def __init__(
            self,
            access_key_id,
            access_key_secret,
            bucket_name,
            endpoint=None,
            cname=None,
            cache_path='.',
            expire_time=30,
            **kwargs
    ):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.bucket_name = bucket_name
        self.endpoint = endpoint

        self.cache_path = cache_path
        self.scheme = kwargs.get("scheme", "https")
        self.image_domain = kwargs.get("image_domain")
        self.asset_domain = kwargs.get("asset_domain")
        self.policy_expire_time = kwargs.get("policy_expire_time", expire_time)

        self.cname = cname

        self.bucket = None

    @abstractmethod
    def create_bucket(self):
        """创建bucket"""

    @abstractmethod
    def list_buckets(self):
        """查询bucket列表"""

    @abstractmethod
    def is_exist_bucket(self, bucket_name=None):
        """判断bucket是否存在"""

    @abstractmethod
    def delete_bucket(self, bucket_name=None):
        """删除bucket"""

    @abstractmethod
    def get_sign_url(self, key, expire=10):
        """生成下载对象的带授权信息的URL"""

    @abstractmethod
    def post_sign_url(self, key, expire=10):
        """生成上传对象的带授权信息的URL"""

    @abstractmethod
    def download(self, *args, **kwargs):
        """"""

    @abstractmethod
    def upload(self, *args, **kwargs):
        """"""

    def _get_policy_encode(self, key, redirect_url):
        expire_time = datetime.datetime.now() + datetime.timedelta(
            seconds=self.policy_expire_time
        )
        policy_dict = dict(
            expiration=expire_time.isoformat() + "Z",
            conditions=[
                # {"acl": "public-read"},
                # {"x-obs-acl": "public-read"},
                # {"x-obs-security-token": "YwkaRTbdY8g7q...."},
                {"bucket": "yzcore"},
                {"success_action_redirect": redirect_url},
                ["starts-with", "$key", key],                         # 指定值开始
                # ["eq", "$success_action_redirect", "public-read"],  # 精确匹配
                # ["content-length-range", 1, 1024*1024*1024]         # 对象大小限制
            ],
        )
        policy = json.dumps(policy_dict).strip().encode()
        return base64.b64encode(policy)

    def get_signature(self, policy_encode):
        """
        获取签名

        :param policy_encode:
        :return:
        """
        h = hmac.new(
            self.access_key_secret.encode("utf-8"), policy_encode, hashlib.sha1
        )
        sign_result = base64.encodebytes(h.digest()).strip()
        return sign_result.decode()

    def get_policy(
            self,
            key,
            redirect_url,
            # callback_data=None,
            # callback_content_type="application/json"
    ):
        """
        授权给第三方上传

        :param key:
        :param redirect_url:
        :return:
        """
        policy_encode = self._get_policy_encode(key, redirect_url)
        sign = self.get_signature(policy_encode)
        return dict(
            key=key,
            accessid=self.access_key_id,
            host=f"{self.scheme}://{self.bucket_name}.{self.endpoint}",
            policy=policy_encode.decode(),
            signature=sign,
            success_action_redirect=redirect_url
            # callback=base64_callback_body.decode(),
        )

    def get_file_url(self, filepath, key):
        if filepath and filepath.split('.')[-1] in IMAGE_FORMAT_SET:
            resource_url = u"//{domain}/{key}".format(
                domain=self.image_domain, key=key)
        else:
            resource_url = u"//{domain}/{key}".format(
                domain=self.asset_domain, key=key)
        return resource_url

    def delete_cache_file(self, filename):
        """删除文件缓存"""
        filepath = os.path.abspath(os.path.join(self.cache_path, filename))
        assert os.path.isfile(filepath), '非文件或文件不存在'
        os.remove(filepath)

    def search_cache_file(self, filename):
        """文件缓存搜索"""
        # 拼接绝对路径
        filepath = os.path.abspath(os.path.join(self.cache_path, filename))
        if os.path.isfile(filepath):
            return filepath
        else:
            return None

    def make_dir(self, dir_path):
        """新建目录"""
        try:
            os.makedirs(dir_path)
        except OSError:
            pass


class OssManagerProxy:
    def __init__(self, oss_type, **kwargs):
        # self.oss_type = oss_type
        self.client = self.select_oss(oss_type, **kwargs)

    def select_oss(self, oss_type, **kwargs):
        _module = import_module(f"yzcore.extensions.oss.{oss_type}")
        return _module.OssManager(**kwargs)

    def __getattr__(self, item):
        return getattr(self.client, item)


