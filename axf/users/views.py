import random

from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from axf.settings import STATIC_URL
from common.func import cookieTORedis, send_email
from orders.models import Order
from users.models import User
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django_redis import get_redis_connection


def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if not user.exists() or not check_password(password,user[0].password):
            return HttpResponse('用户名或密码错误')

        request.session['username'] = username

        res = redirect(reverse('users:info'))

        return cookieTORedis(request,res)

    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        #接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        avatar = request.FILES.get('avatar')
        phone = request.POST.get('phone')
        smscode = request.POST.get('smscode')

        #判断用户名是否已经存在
        # User.objects.filter(username=username).count()

        # try:
        #     User.objects.get(username=username)
        # except User.DoesNotExist:
        #     pass
        res = User.objects.filter(username=username).exists()
        if res:
            return HttpResponse('用户名已存在')
        if password != password_confirm:
            return HttpResponse('密码输入不一致')

        #验证验证码是否正确
        # redis_cli = get_redis_connection()
        # code = redis_cli.get(f"sms-{phone}")
        # if not code:
        #     return HttpResponse("验证码已失效，请重新发送")
        # if smscode != code.decede():
        #     return HttpResponse("验证码错误")

        #逻辑处理，将用户信息添加到用户表中
        User.objects.create(
            username=username,
            password=make_password(password), #加密密码
            phone=phone,
            avatar=avatar  # 新增的数据的时候，自动上传图片
        )


        #将图片存储在第三方应用七牛上
        # upload_to_qiniu(avatar.name, os.path.join(settings.MEDIA_ROOT, 'uploads', avatar.name))
        #
        # user.avatar = 'http://py25tqtvc.bkt.clouddn.com/' + avatar.name
        #
        # user.save()


        #返回响应,跳转到登录页面
        return redirect(reverse("users:login"))

    else:
        return render(request,'register.html')




# 发送短信
def sendsms(request):
    smscode = random.randint(1000, 9999)
    phone = request.POST.get('phone')

    data = {
        "sid": "8036ece41e07ea5340794286185f9214",
        "token": "8a9c9099eb825ea314bcb620f9fdbc6b",
        "appid": "cceff1236cee4e1e87b87186dc10ad27",
        "templateid": "493813",
        "param": smscode,
        "mobile": phone,
    }

    # 用云之讯第三方发短信
    res = requests.post('https://open.ucpaas.com/ol/sms/sendsms', json=data)

    res = res.json()

    if res['code'] == '000000':

        # 保存验证码，保存在缓存里面，给一个过期时间
        # 实例化redis
        redis_cli = get_redis_connection()

        redis_cli.set(f'sms_{phone}', smscode, 180)

        return JsonResponse({'res': 'yes'})
    else:
        return JsonResponse({'res': 'no'})


def info(request):
    #判断用户是否登录
    login = False
    user = ''
    # no_pay_count = 0
    # no_receive_count = 0
    no_pay = 0
    no_receive = 0
    jpg_path = ''
    if request.session.get('username'):
        login = True
        username = request.session.get('username')
        user = User.objects.get(username=username)

        # print(user.avatar)

        #查询物品状态，1为未付款，3为未收货
        no_pay = Order.objects.filter(uid=user.id, status=1).count()
        no_receive = Order.objects.filter(uid=user.id, status=3).count()

        jpg_path = STATIC_URL+str(user.avatar)


    context = {
        'login' : login,
        'user' : user,
        'no_pay': no_pay,
        'no_receive': no_receive,
        'jpg_show':jpg_path
        # 'no_pay_count' : no_pay_count,
        # 'no_receive_count' : no_receive_count
    }

    return render(request,'mine.html',context)


def logout(request):

    #退出登录,清除session
    del request.session['username']
    return redirect(reverse('users:login'))


def email(request):

    if request.method == "GET":
        username = request.session.get('username')
        user = User.objects.get(username=username)
        context = {
            'user':user
        }
        return render(request,'email.html',context)
    else:
        email = request.POST.get('email')
        # print('email=',email)
        type = request.POST.get('type')

        if type == '1':
            #保存邮箱操作
            username = request.session.get('username')
            User.objects.filter(username=username).update(email=email)

            return redirect(reverse('users:email'))

        elif type == '2':
            #激活邮箱操作
            # 发送邮件
            email = request.POST.get('email_active')

            send_email.delay(email)  #将任务放入队列

            return HttpResponse('邮箱发送成功，请点击激活')

def active(request):
    #接收邮箱，激活邮箱
    email = request.GET.get('email')
    User.objects.filter(email=email).update(is_active=1)

    return redirect(reverse('users:email'))