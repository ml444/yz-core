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
try:
    import oss2
except:
    pass

__all__ = [
    "OssManager", "OssManagerError"
]
IMAGE_FORMAT_SET = [
    'bmp', 'jpg', 'jpeg', 'png', 'tif', 'gif', 'pcx', 'tga',
    'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo',
    'eps', 'ai', 'raw', 'WMF', 'webp', 'tiff'
]

OssManagerError = type("OssManagerError", (ValueError,), {})


class OssManager(object):
    """
    使用示例:
        >>> from . import OssManager
        >>> oss_conf = dict(
        ...     access_key_id="LTAIpU4LFStTy95Q",
        ...     access_key_secret="Cep4MBhQpeB8cSNpv6w5nD8OMhOSUA",
        ...     endpoint="oss-cn-shenzhen.aliyuncs.com",
        ...     # endpoint="oss-cn-shenzhen-internal.aliyuncs.com",
        ...     bucket_name="realicloud-local",
        ...     cache_path="/tmp/realicloud/fm/cache"
        ... )

        >>> oss = OssManager(**oss_conf)
        >>> oss.upload("/home/zhangw/Work/模型文件/狼.fbx", "test/狗.fbx")
        >>> oss.download("test/狗.fbx")
    """
    def __init__(
            self,
            access_key_id,
            access_key_secret,
            endpoint,
            bucket_name,
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

        self.bucket = None
        self.__init()

    def __init(self):
        """初始化对象"""
        assert oss2 is not None, "'oss2' must be installed to use OssManager"
        oss_auth = oss2.Auth(self.access_key_id, self.access_key_secret)

        self.bucket = oss2.Bucket(
            oss_auth, self.endpoint, self.bucket_name
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

    def download(self, key, local_name=None, process=None, is_stream=False):
        """
        下载oss文件

        :param key:
        :param local_name:
        :param process:
        :param is_stream:
            is_stream = True:
                >>> result = self.download('readme.txt', is_stream=True)
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
        if is_stream:
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
            return result.resp.response.url
        return self.get_file_url(filepath, key)

    def get_policy(
            self,
            filepath,
            callback_url,
            callback_data=None,
            callback_content_type="application/json"):
        """
        授权给第三方上传

        :param filepath:
        :param callback_url:
        :param callback_data: 需要回传的参数
        :param callback_content_type: 回调时的Content-Type
               "application/json"
               "application/x-www-form-urlencoded"

        :return:
        """
        params = urllib.parse.urlencode(
            dict(data=json.dumps(callback_data)))
        policy_encode = self._get_policy_encode(filepath)
        sign = self.get_signature(policy_encode)

        callback_dict = dict()
        callback_dict["callbackUrl"] = callback_url
        callback_dict["callbackBody"] = (
            "filepath=${object}&size=${size}&mime_type=${mimeType}"
            "&img_height=${imageInfo.height}&img_width=${imageInfo.width}"
            "&img_format=${imageInfo.format}&" + params
        )
        callback_dict["callbackBodyType"] = callback_content_type

        callback_param = json.dumps(callback_dict).strip().encode()
        base64_callback_body = base64.b64encode(callback_param)

        return dict(
            accessid=self.access_key_id,
            host=f"{self.scheme}://{self.bucket_name}.{self.endpoint}",
            policy=policy_encode.decode(),
            signature=sign,
            dir=filepath,
            callback=base64_callback_body.decode(),
        )

    def _get_policy_encode(self, filepath):
        expire_time = datetime.datetime.now() + datetime.timedelta(
            seconds=self.policy_expire_time
        )
        policy_dict = dict(
            expiration=expire_time.isoformat() + "Z",
            conditions=[["starts-with", "$key", filepath]],
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

    def get_file_url(self, filepath, key):
        if filepath.split('.')[-1] in IMAGE_FORMAT_SET:
            resource_url = u"//{domain}/{key}".format(
                domain=self.image_domain, key=key)
        else:
            resource_url = u"//{domain}/{key}".format(
                domain=self.asset_domain, key=key)
        return resource_url

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