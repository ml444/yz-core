#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021/3/8
@desc: ...
"""
import os
import functools
from yzcore.extensions.oss import OssManagerBase, OssRequestError
# from obs import ObsClient, StorageClass, HeadPermission
try:
    import obs
except:
    obs = None


def wrap_request_return_bool(func):
    """"""
    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            if resp.status < 300:
                return True
            else:
                return False
        except:
            import traceback
            print(traceback.format_exc())
    return wrap_func


class OssManager(OssManagerBase):
    acl_type = {
        "private": obs.HeadPermission.PRIVATE,
        "onlyread": obs.HeadPermission.PUBLIC_READ,
        "readwrite": obs.HeadPermission.PUBLIC_READ_WRITE,
        "bucket_read": obs.HeadPermission.PUBLIC_READ_DELIVERED,                # 桶公共读，桶内对象公共读。
        "bucket_readwrite": obs.HeadPermission.PUBLIC_READ_WRITE_DELIVERED,     # 桶公共读写，桶内对象公共读写。
        "owner_full_control": obs.HeadPermission.BUCKET_OWNER_FULL_CONTROL,     # 桶或对象所有者拥有完全控制权限。
    }
    # 存储类型
    storage_cls = {
        "standard": obs.StorageClass.STANDARD,              # 标准类型
        "ia": obs.StorageClass.WARM,                        # 低频访问类型
        # "archive": oss2.BUCKET_STORAGE_CLASS_ARCHIVE,  # 归档类型
        "cold_archive": obs.StorageClass.COLD,              # 冷归档类型
    }
    # 冗余类型
    # redundancy_type = {
    #     "lrs": oss2.BUCKET_DATA_REDUNDANCY_TYPE_LRS,  # 本地冗余
    #     "zrs": oss2.BUCKET_DATA_REDUNDANCY_TYPE_ZRS,  # 同城冗余（跨机房）
    # }

    def __init__(self, *args, **kwargs):
        super(OssManager, self).__init__(*args, **kwargs)
        self.__init()

    def __init(self, *args, **kwargs):
        """"""
        if obs is None:
            raise ImportError("'esdk-obs-python' must be installed to use OssManager")
        # 创建ObsClient实例
        self.obsClient = obs.ObsClient(
            access_key_id=self.access_key_id,
            secret_access_key=self.access_key_secret,
            server=self.endpoint
        )
        # self.bucket = self.obsClient.bucketClient(self.bucket_name)

    def create_bucket(
            self, bucket_name=None, location='cn-south-1'
    ):
        """"""
        if bucket_name is None:
            bucket_name = self.bucket_name
        resp = self.obsClient.createBucket(bucket_name, location=location)
        if resp.status < 300:
            return True
        else:
            raise OssRequestError(
                f"errorCode: {resp.errorCode}. Message: {resp.errorMessage}.")

    def list_buckets(self):
        resp = self.obsClient.listBuckets(isQueryLocation=True)
        if resp.status < 300:
            return resp.body.buckets
        else:
            raise OssRequestError(
                f"errorCode: {resp.errorCode}. Message: {resp.errorMessage}.")

    @wrap_request_return_bool
    def is_exist_bucket(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        return self.obsClient.headBucket(bucket_name)

    @wrap_request_return_bool
    def delete_bucket(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        return self.obsClient.deleteBucket(bucket_name)

    def get_sign_url(self, key, expire=10):
        res = self.obsClient.createSignedUrl("GET", self.bucket_name, key, expire)
        return res.signedUrl

    def post_sign_url(self, key, expire=10, form_param=None):
        if form_param:
            return self.obsClient.createPostSignature(
                self.bucket_name, key, expire, formParams=form_param)
        else:
            res = self.obsClient.createSignedUrl(
                "PUT", self.bucket_name, key, expire)
            return res.signedUrl

    def download(self, key, local_name=None,
                 is_return_obj=False, progress_callback=None):
        if not local_name:
            local_name = os.path.abspath(
                os.path.join(self.cache_path, key)
            )
        self.make_dir(os.path.dirname(local_name))
        try:
            resp = self.obsClient.getObject(
                self.bucket_name, key,
                downloadPath=local_name,
                progressCallback=progress_callback
            )

            if resp.status < 300:
                if is_return_obj:
                    with open(local_name, 'rb') as fileobj:
                        return fileobj
                return resp.body.url  # url: /Users/edz/yz-core/tests/cml
            else:
                print('errorCode:', resp.errorCode)
                print('errorMessage:', resp.errorMessage)
        except:
            import traceback
            print(traceback.format_exc())

    def get_file_stream(self, key, bucket_name=None):
        try:
            resp = self.obsClient.getObject(
                self.bucket_name, key,
                loadStreamInMemory=True,
            )
            if resp.status < 300:
                print('requestId:', resp.requestId)
                # 获取对象内容
                print('size:', resp.body.size)
                return resp.body.buffer
            else:
                print('errorCode:', resp.errorCode)
                print('errorMessage:', resp.errorMessage)
        except:
            import traceback
            print(traceback.format_exc())

    def upload(self, key=None, filepath=None, content=None):
        if not any((filepath, content)):
            raise ValueError("not any((filepath, content))")
        if key is None and filepath:
            key = filepath.split('/')[-1]
        try:
            if content:
                resp = self.obsClient.putContent(
                    self.bucket_name, key, content=content)
            else:
                resp = self.obsClient.putFile(
                    self.bucket_name, key, filepath)
            if resp.status < 300:
                print('requestId:', resp.requestId)
                return True, self.get_file_url(filepath, key)
            else:
                print('errorCode:', resp.errorCode)
                print('errorMessage:', resp.errorMessage)
                return False, None
        except:
            import traceback
            print(traceback.format_exc())

    # def close_client(self):
    #     return self.obsClient.close()






