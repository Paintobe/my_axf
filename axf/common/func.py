import json

from qiniu import Auth, put_file
from django_redis import get_redis_connection

def upload_to_qiniu(filename, localfile):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'bbs0RlgZlWGB_PwIyKrZQVFdZvwex9m6uoAVbMTE'
    secret_key = 'd3UQGh89TNPjjxxKDbdD4lznlTqDtIw4er-J6crX'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'sz1905'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)
    ret, info = put_file(token, filename, localfile)
    print(info)
    return info






