import json

from django.conf import settings
from django.core.mail import send_mail
from qiniu import Auth, put_file
from django_redis import get_redis_connection
from worker import celery_app


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


#合并cookie中的购物数据到redis中
def cookieTORedis(request,response):

    #取出cookie中的数据
    cookie_data = request.COOKIES.get('cookie_data')

    #取出redis中的数据
    username = request.session.get('username')
    redis_cli = get_redis_connection('cart')
    redis_data = redis_cli.get(f'cart_{username}')

    if cookie_data:
        if not redis_data:
            redis_data = cookie_data
        else:
            cookie_data = json.loads(cookie_data)
            # print(cookie_data)
            redis_data = json.loads(redis_data)
            # print(redis_data)
            #将cookie中的数据更新到redis中
            redis_data.update(cookie_data)
            # print(redis_data)

            redis_data = json.dumps(redis_data)
        redis_cli.set(f'cart_{username}',redis_data)

        response.delete_cookie('cookie_data')

    return response


@celery_app.task
def send_email(email):
    to_email = email
    verify_url = 'http://127.0.0.1:8000/active/?email=' + email
    subject = "激活邮箱"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)

    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)



