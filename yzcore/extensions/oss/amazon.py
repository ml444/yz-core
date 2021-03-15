#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021/3/12
@desc: ...
"""
import os
import functools
from yzcore.extensions.oss import OssManagerBase, OssRequestError
# from obs import ObsClient, StorageClass, HeadPermission
try:
    import boto3
except:
    boto3 = None


def wrap_request_return_bool(func):
    """"""
    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            if resp['ResponseMetadata']['HTTPStatusCode'] < 300:
                return True
            else:
                return False
        except:
            import traceback
            print(traceback.format_exc())
    return wrap_func


class OssManager(OssManagerBase):
    # acl_type = {
    #     "private": obs.HeadPermission.PRIVATE,
    #     "onlyread": obs.HeadPermission.PUBLIC_READ,
    #     "readwrite": obs.HeadPermission.PUBLIC_READ_WRITE,
    #     "bucket_read": obs.HeadPermission.PUBLIC_READ_DELIVERED,                # 桶公共读，桶内对象公共读。
    #     "bucket_readwrite": obs.HeadPermission.PUBLIC_READ_WRITE_DELIVERED,     # 桶公共读写，桶内对象公共读写。
    #     "owner_full_control": obs.HeadPermission.BUCKET_OWNER_FULL_CONTROL,     # 桶或对象所有者拥有完全控制权限。
    # }
    # # 存储类型
    # storage_cls = {
    #     "standard": obs.StorageClass.STANDARD,              # 标准类型
    #     "ia": obs.StorageClass.WARM,                        # 低频访问类型
    #     # "archive": oss2.BUCKET_STORAGE_CLASS_ARCHIVE,  # 归档类型
    #     "cold_archive": obs.StorageClass.COLD,              # 冷归档类型
    # }
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
        if boto3 is None:
            raise ImportError("'boto3' must be installed to use OssManager")
        # 创建ObsClient实例
        self.client = boto3.client(
            's3',
            # region_name=None,
            # api_version=None,
            # use_ssl=True,
            # verify=None,
            # endpoint_url=None,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.access_key_secret,
            # aws_session_token=None,
            # config=None
        )
        # self.bucket = self.client.bucketClient(self.bucket_name)

    @wrap_request_return_bool
    def create_bucket(
            self, bucket_name=None, location='cn-south-1'
    ):
        """"""
        if bucket_name is None:
            bucket_name = self.bucket_name
        return self.client.create_bucket(
            ACL='private',  # |'public-read'|'public-read-write'|'authenticated-read',
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'cn-northwest-1',  # 'cn-north-1'
            },
            # GrantFullControl='string',
            # GrantRead='string',
            # GrantReadACP='string',
            # GrantWrite='string',
            # GrantWriteACP='string',
            # ObjectLockEnabledForBucket=True|False
        )
        # if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
        #     return True

    def list_buckets(self):
        """

        :return: {
            'Buckets': [
                {
                    'Name': 'string',
                    'CreationDate': datetime(2015, 1, 1)
                },
            ],
            'Owner': {
                'DisplayName': 'string',
                'ID': 'string'
            }
        }
        """
        return self.client.list_buckets()

    @wrap_request_return_bool
    def is_exist_bucket(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        return self.client.head_bucket(
            Bucket=bucket_name,
            # ExpectedBucketOwner='string'
        )

    @wrap_request_return_bool
    def delete_bucket(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        return self.client.delete_bucket(
            Bucket=bucket_name,
            # ExpectedBucketOwner='string'
        )

    def get_sign_url(self, key, expire=10):
        res = self.client.createSignedUrl("GET", self.bucket_name, key, expire)
        return res.signedUrl

    def post_sign_url(self, key, expire=10, form_param=None):
        if form_param:
            return self.client.createPostSignature(
                self.bucket_name, key, expire, formParams=form_param)
        else:
            res = self.client.createSignedUrl(
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
            if is_return_obj:
                with open(local_name, 'wb') as fileobj:
                    self.client.download_fileobj(
                        self.bucket_name, key, fileobj,
                        Callback=progress_callback)
                    return fileobj
            else:
                self.client.download_file(
                    self.bucket_name, key, local_name,
                    Callback=progress_callback)
                return local_name
        except:
            import traceback
            print(traceback.format_exc())

    def get_file_stream(self, key, bucket_name=None):
        return self.client.get_object(
            Bucket=bucket_name if bucket_name else self.bucket_name,
            Key=key,
            # Range='string',
            # IfMatch='string',
            # IfModifiedSince=datetime(2015, 1, 1),
            # IfNoneMatch='string',
            # IfUnmodifiedSince=datetime(2015, 1, 1),
            # ResponseCacheControl='string',
            # ResponseContentDisposition='string',
            # ResponseContentEncoding='string',
            # ResponseContentLanguage='string',
            # ResponseContentType='string',
            # ResponseExpires=datetime(2015, 1, 1),
            # VersionId='string',
            # SSECustomerAlgorithm='string',
            # SSECustomerKey='string',
            # RequestPayer='requester',
            # PartNumber=123,
            # ExpectedBucketOwner='string'
        )

    def upload(self, key=None, filepath=None, content=None):
        if not any((filepath, content)):
            raise ValueError("not any((filepath, content))")
        if key is None and filepath:
            key = filepath.split('/')[-1]
        try:
            if content:
                resp = self.client.upload_fileobj(
                    content, self.bucket_name, key)
            else:
                resp = self.client.upload_file(
                    filepath, self.bucket_name, key)
            print(resp)
            return True, self.get_file_url(filepath, key)
        except:
            import traceback
            print(traceback.format_exc())
            return False, None

    # def get_policy2(self):
    #     # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_post
    #     return self.client.generate_presigned_post(
    #         Bucket, Key, Fields=None, Conditions=None, ExpiresIn=3600)

    # def close_client(self):
    #     return self.client.close()






