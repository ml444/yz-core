#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-10-20
@desc: 对阿里云oss的封装，依赖oss2

配置文件：
    [oss_manager]
    access_key_id = XXXXX
    access_key_secret = XXXXX
    endpoint = oss-cn-shenzhen.aliyuncs.com
    # internal_endpoint = oss-cn-shenzhen-internal.aliyuncs.com
    bucket_name = bucket_name
    image_domain = internal.image.realibox.com
    asset_domain = internal.asset.realibox.com
    expire_time = 30
    cache_path = /tmp/xxxx/cache/
"""

import os
import shutil
import json
import base64
import hmac
import datetime
import hashlib
import urllib
from enum import Enum
try:
    import oss2
except:
    oss2 = None

from . import OssManagerBase

__all__ = [
    "OssManager", "OssManagerError"
]


OssManagerError = type("OssManagerError", (ValueError,), {})


# class ACL(Enum):
#     private = oss2.BUCKET_ACL_PRIVATE
#     onlyread = oss2.BUCKET_ACL_PUBLIC_READ
#     readwrite = oss2.BUCKET_ACL_PUBLIC_READ_WRITE


class OssManager(OssManagerBase):
    """
    使用示例:
        >>> from . import OssManager
        >>> oss_conf = dict(
        ...     access_key_id="LTAIxxxxxxxxxxx",
        ...     access_key_secret="Cep4Mxxxxxxxxxxxxxxxxxxxx",
        ...     endpoint="oss-cn-shenzhen.aliyuncs.com",
        ...     # endpoint="oss-cn-shenzhen-internal.aliyuncs.com",
        ...     bucket_name="xxxx-local",
        ...     cache_path="/tmp/xxxx/fm/cache"
        ... )

        >>> oss = OssManager(**oss_conf)
        >>> oss.upload("/home/zhangw/Work/模型文件/狼.fbx", "test/狗.fbx")
        >>> oss.download("test/狗.fbx")
    """

    acl_type = {
        "private": oss2.BUCKET_ACL_PRIVATE,
        "onlyread": oss2.BUCKET_ACL_PUBLIC_READ,
        "readwrite": oss2.BUCKET_ACL_PUBLIC_READ_WRITE,
    }
    # 存储类型
    storage_cls = {
        "standard": oss2.BUCKET_STORAGE_CLASS_STANDARD,          # 标准类型
        "ia": oss2.BUCKET_STORAGE_CLASS_IA,                      # 低频访问类型
        "archive": oss2.BUCKET_STORAGE_CLASS_ARCHIVE,            # 归档类型
        "cold_archive": oss2.BUCKET_STORAGE_CLASS_COLD_ARCHIVE,  # 冷归档类型
    }
    # 冗余类型
    redundancy_type = {
        "lrs": oss2.BUCKET_DATA_REDUNDANCY_TYPE_LRS,    # 本地冗余
        "zrs": oss2.BUCKET_DATA_REDUNDANCY_TYPE_ZRS,    # 同城冗余（跨机房）
    }

    def __init__(self, *args, **kwargs):
        super(OssManager, self).__init__(*args, **kwargs)

    def __init(self, bucket_name=None):
        """初始化对象"""
        if oss2 is None:
            raise ImportError("'oss2' must be installed to use OssManager")
        if not any((self.endpoint, self.cname)):
            raise AttributeError(
                "One of 'endpoint' and 'cname' must not be None.")

        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)

        # 如果cname存在，则使用自定义域名初始化
        self.endpoint = self.cname if self.cname else self.endpoint
        is_cname = True if self.cname else False
        self.bucket_name = bucket_name if bucket_name else self.bucket_name
        self.bucket = oss2.Bucket(
            self.auth, self.endpoint, self.bucket_name, is_cname=is_cname
        )

        if self.cache_path:
            try:
                os.makedirs(self.cache_path)
            except OSError:
                pass
            # make_dir(self.cache_path)

    def reload_oss(self, **kwargs):
        """重新加载oss配置"""
        self.access_key_id = kwargs.get("access_key_id")
        self.access_key_secret = kwargs.get("access_key_secret")
        self.bucket_name = kwargs.get("bucket_name")
        self.endpoint = kwargs.get("endpoint")
        self.__init()

    def create_bucket(self, bucket_name=None,
                      acl_type='private',
                      storage_type='standard',
                      redundancy_type='zrs'):
        self.__init(bucket_name=bucket_name)
        permission = self.acl_type.get(acl_type)
        config = oss2.models.BucketCreateConfig(
            storage_class=self.storage_cls.get(storage_type),
            data_redundancy_type=self.redundancy_type.get(redundancy_type)
        )
        return self.bucket.create_bucket(permission, input=config)

    def iter_buckets(self, prefix='', marker='', max_keys=100, max_retries=None):
        """
        :param prefix: 只列举匹配该前缀的Bucket
        :param marker: 分页符。只列举Bucket名字典序在此之后的Bucket
        :param max_keys: 每次调用 `list_buckets` 时的max_keys参数。注意迭代器返回的数目可能会大于该值。
        :param max_retries:
        :return:
        """
        if not hasattr(self, 'service'):
            self.service = oss2.Service(self.auth, self.endpoint)

        return oss2.BucketIterator(
            self.service, prefix=prefix, marker=marker,
            max_keys=max_keys, max_retries=max_retries)

    def list_buckets(self, prefix='', marker='', max_keys=100, params=None):
        """根据前缀罗列用户的Bucket。

        :param str prefix: 只罗列Bucket名为该前缀的Bucket，空串表示罗列所有的Bucket
        :param str marker: 分页标志。首次调用传空串，后续使用返回值中的next_marker
        :param int max_keys: 每次调用最多返回的Bucket数目
        :param dict params: list操作参数，传入'tag-key','tag-value'对结果进行过滤

        :return: 罗列的结果
        :rtype: oss2.models.ListBucketsResult
        """
        if not hasattr(self, 'service'):
            self.service = oss2.Service(self.auth, self.endpoint)
        return self.service.list_buckets(
            prefix=prefix, marker=marker, max_keys=max_keys, params=params)

    def is_exist_bucket(self):
        """判断存储空间是否存在"""
        try:
            self.bucket.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            return False
        except:
            raise
        return True

    def delete_bucket(self, bucket_name=None):
        """删除bucket"""
        try:
            resp = self.bucket.delete_bucket()
            if resp.status < 300:
                return True
            elif resp.status == 404:
                return False
        except:
            import traceback
            print(traceback.format_exc())

    # def encrypt_bucket(self):
    #     """设置Bucket加密"""
    #     # 创建Bucket加密配置，以AES256加密为例。
    #     rule = oss2.models.ServerSideEncryptionRule()
    #     rule.sse_algorithm = oss2.SERVER_SIDE_ENCRYPTION_AES256
    #     # 设置KMS密钥ID，加密方式为KMS可设置此项。
    #     # 如需使用指定的密钥加密，需输入指定的CMK ID；
    #     # 若使用OSS托管的CMK进行加密，此项为空。使用AES256进行加密时，此项必须为空。
    #     rule.kms_master_keyid = ""
    #
    #     # 设置Bucket加密。
    #     result = self.bucket.put_bucket_encryption(rule)
    #     # 查看HTTP返回码。
    #     print('http response code:', result.status)
    #     return result
    #
    # def delete_encrypt_bucket(self):
    #     # 删除Bucket加密配置。
    #     result = self.bucket.delete_bucket_encryption()
    #     # 查看HTTP返回码。
    #     print('http status:', result.status)
    #     return result

    def get_sign_url(self, key, expire=10):
        return self.bucket.sign_url("GET", key, expire)

    def post_sign_url(self, key, expire=10):
        return self.bucket.sign_url("POST", key, expire)

    def download(self, key, local_name=None,
                 is_return_obj=False,
                 progress_callback=None, process=None):
        """
        下载oss文件

        :param key:
        :param local_name:
        :param process:
        :param load_stream_in_memory:
            is_stream = True:
                >>> result = self.download('readme.txt', load_stream_in_memory=True)
                >>> print(result.read())
                'hello world'
            is_stream = False:
                >>> result = self.download('readme.txt', '/tmp/cache/readme.txt')
                >>> print(result)
                '/tmp/cache/readme.txt'
        :return:
        """
        if not local_name:
            local_name = os.path.abspath(
                os.path.join(self.cache_path, key)
            )
        make_dir(os.path.dirname(local_name))
        if is_return_obj:
            return self.bucket.get_object(key, process=process)
        else:
            self.bucket.get_object_to_file(key, local_name, process=process)
            return local_name

    def upload(self, filepath, key=None, num_threads=2):
        """上传oss文件"""
        if key is None:
            key = filepath.split('/')[-1]
        headers = None
        if filepath.endswith(".dds"):
            headers = dict()
            headers["Content-Type"] = "application/octet-stream"

        result = oss2.resumable_upload(
            self.bucket, key, filepath,
            headers=headers,
            num_threads=num_threads,
        )
        # 返回下载链接
        if not any((self.image_domain, self.asset_domain)):
            return True, result.resp.response.url
        return True, self.get_file_url(filepath, key)

    # def get_policy(
    #         self,
    #         filepath,
    #         callback_url,
    #         callback_data=None,
    #         callback_content_type="application/json"):
    #     """
    #     授权给第三方上传
    #
    #     :param filepath:
    #     :param callback_url:
    #     :param callback_data: 需要回传的参数
    #     :param callback_content_type: 回调时的Content-Type
    #            "application/json"
    #            "application/x-www-form-urlencoded"
    #
    #     :return:
    #     """
    #     params = urllib.parse.urlencode(
    #         dict(data=json.dumps(callback_data)))
    #     policy_encode = self._get_policy_encode(filepath)
    #     sign = self.get_signature(policy_encode)
    #
    #     callback_dict = dict()
    #     callback_dict["callbackUrl"] = callback_url
    #     callback_dict["callbackBody"] = (
    #         "filepath=${object}&size=${size}&mime_type=${mimeType}"
    #         "&img_height=${imageInfo.height}&img_width=${imageInfo.width}"
    #         "&img_format=${imageInfo.format}&" + params
    #     )
    #     callback_dict["callbackBodyType"] = callback_content_type
    #
    #     callback_param = json.dumps(callback_dict).strip().encode()
    #     base64_callback_body = base64.b64encode(callback_param)
    #
    #     return dict(
    #         accessid=self.access_key_id,
    #         host=f"{self.scheme}://{self.bucket_name}.{self.endpoint}",
    #         policy=policy_encode.decode(),
    #         signature=sign,
    #         dir=filepath,
    #         callback=base64_callback_body.decode(),
    #     )
    #
    # def _get_policy_encode(self, filepath):
    #     expire_time = datetime.datetime.now() + datetime.timedelta(
    #         seconds=self.policy_expire_time
    #     )
    #     policy_dict = dict(
    #         expiration=expire_time.isoformat() + "Z",
    #         conditions=[
    #             ["starts-with", "$key", filepath],                    # 指定值开始
    #             # ["eq", "$success_action_redirect", "public-read"],  # 精确匹配
    #             # ["content-length-range", 1, 1024*1024*1024]         # 对象大小限制
    #         ],
    #     )
    #     policy = json.dumps(policy_dict).strip().encode()
    #     return base64.b64encode(policy)
    #
    # def get_signature(self, policy_encode):
    #     """
    #     获取签名
    #
    #     :param policy_encode:
    #     :return:
    #     """
    #     h = hmac.new(
    #         self.access_key_secret.encode("utf-8"), policy_encode, hashlib.sha1
    #     )
    #     sign_result = base64.encodebytes(h.digest()).strip()
    #     return sign_result.decode()

    def update_file_headers(self, key, headers):
        self.bucket.update_object_meta(key, headers)





def make_dir(dir_path):
    """新建目录"""
    try:
        os.makedirs(dir_path)
    except OSError:
        pass


def copy_file(src, dst):
    """拷贝文件"""
    dst_dir = os.path.dirname(dst)
    make_dir(dst_dir)
    shutil.copy(src, dst)


if __name__ == '__main__':
    kwargs = dict(
        access_key_id='',
        access_key_secret='',
        endpoint='oss-cn-shenzhen.aliyuncs.com',
        bucket_name='',
    )
    oss_obj = OssManager(**kwargs)
    file_name = '/Users/edz/realibox/base-all/base/src/core/request/beta_gangnam_style.fbx'
    # remote_name = 'cmltest.fbx'

    # 上传
    result_obj = oss_obj.upload(file_name)
    print(result_obj)
    """
    http://realicloud-local.oss-cn-shenzhen.aliyuncs.com/beta_gangnam_style.fbx
    """

    """
    # result:
    {
        'resp': <oss2.http.Response object at 0x1071ddc50>, 
        'status': 200, 
        'headers': {
            'Server': 'AliyunOSS', 
            'Date': 'Tue, 20 Oct 2020 01:22:34 GMT', 
            'Content-Length': '0', 
            'Connection': 'keep-alive', 
            'x-oss-request-id': '5F8E3BDAFEC931303087D9D9', 
            'ETag': '"D41D8CD98F00B204E9800998ECF8427E"', 
            'x-oss-hash-crc64ecma': '0', 
            'Content-MD5': '1B2M2Y8AsgTpgAmY7PhCfg==', 
            'x-oss-server-time': '63'
        }, 
        'request_id': '5F8E3BDAFEC931303087D9D9', 
        'versionid': None, 
        'delete_marker': None, 
        'etag': 'D41D8CD98F00B204E9800998ECF8427E', 
        'crc': 0
    }
    
    # result.resp:
    {
        'response': <Response [200]>, 
        'status': 200, 
        'headers': {
            'Server': 'AliyunOSS', 
            'Date': 'Tue, 20 Oct 2020 02:31:03 GMT', 
            'Content-Length': '0', 
            'Connection': 'keep-alive', 
            'x-oss-request-id': '5F8E4BE7FEC93130387B8D5B', 
            'ETag': '"D41D8CD98F00B204E9800998ECF8427E"', 
            'x-oss-hash-crc64ecma': '0', 
            'Content-MD5': '1B2M2Y8AsgTpgAmY7PhCfg==', 
            'x-oss-server-time': '49'
        }, 
        'request_id': '5F8E4BE7FEC93130387B8D5B', 
        '_Response__all_read': True
    }
    
    # result.resp.response:
    {
        '_content': False, 
        '_content_consumed': True, 
        '_next': None, 
        'status_code': 200, 
        'headers': {
            'Server': 'AliyunOSS', 
            'Date': 'Tue, 20 Oct 2020 02:32:13 GMT', 
            'Content-Length': '0', 
            'Connection': 'keep-alive', 
            'x-oss-request-id': '5F8E4C2D4D5A2B3339F164B7', 
            'ETag': '"D41D8CD98F00B204E9800998ECF8427E"', 
            'x-oss-hash-crc64ecma': '0', 
            'Content-MD5': '1B2M2Y8AsgTpgAmY7PhCfg==', 
            'x-oss-server-time': '18'
        }, 
        'raw': <urllib3.response.HTTPResponse object at 0x104254a10>, 
        'url': 'http://haier-mdcp-private.oss-cn-qingdao.aliyuncs.com/cmltest.fbx', 
        'encoding': None, 
        'history': [], 
        'reason': 'OK', 
        'cookies': <RequestsCookieJar[]>, 
        'elapsed': datetime.timedelta(microseconds=250406), 
        'request': <PreparedRequest [PUT]>, 
        'connection': <requests.adapters.HTTPAdapter object at 0x1041fb710>
    }
    
    """

    # 下载
    # res = oss_obj.download(remote_name)
    # print(res)