import json

from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection

# Create your views here.
from market.models import Goods


def index(request):
    if request.session.get('username'):
        username = request.session.get('username')
        redis_cli = get_redis_connection('cart')
        data = redis_cli.get(f'cart_{username}')
    else:
        #取出cookie中的数据
        data = request.COOKIES.get('cookie_data')

    #初始化总价
    totalprice = 0
    #判断cookie是否有数据
    data_list = []
    if data:
        data = json.loads(data)
        for d in data:
            goods = Goods.objects.get(id=d)
            data_dict = {
                'id' : goods.id,
                'img' : goods.productimg,
                'name' : goods.productlongname,
                'price' : goods.price,
                'num' : data[d]['count'],
                'selected' : data[d]['selected']
            }

            data_list.append(data_dict)

            if data[d]['selected'] == '1':
                totalprice += goods.price*int(data[d]['count'])

    context = {
        'data_list' : data_list,
        'totalprice' : totalprice
    }
    return render(request,'cart.html',context)


def selects(request):
    #获取selects的值
    selected = request.POST.get('selected')
    if request.session.get('username'):
        username = request.session.get('username')
        redis_cli = get_redis_connection('cart')
        cookie_data = redis_cli.get(f'cart_{username}')

    else:
        #获取cookie_data值
        cookie_data = request.COOKIES.get('cookie_data')

    #将cookie_data转为字典形式
    cookie_data = json.loads(cookie_data)

    for data in cookie_data:
        cookie_data[data]['selected'] = selected

    #将cookie_data转为json字符串
    cookie_data = json.dumps(cookie_data)

    #重设cookie_data
    res = HttpResponse({'data':'ok'})

    if request.session.get('username'):
        redis_cli.set(f'cart_{username}',cookie_data)
    else:
        res.set_cookie('cookie_data',cookie_data)

    return res