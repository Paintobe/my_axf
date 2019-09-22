import json
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django_redis import get_redis_connection

from market.models import Goods
from .models import Order,OrderDetail

from users.models import User


# Create your views here.
from django.urls import reverse


def index(request):

    #判断用户是否登录
    if not request.session.get('username'):
        return redirect(reverse('users:login'))


    #生成订单逻辑
    #取出redis中购物数据
    redis_cli = get_redis_connection('cart')
    username = request.session.get('username')
    cart_data = redis_cli.get(f'cart_{username}')
    cart_data = json.loads(cart_data)

    cart_dict = {}
    for cart in cart_data:
        if cart_data[cart]['selected'] == '1':
            # {'gid1':'count1', 'gid2':'count2'}
            cart_dict[int(cart)] = int(cart_data[cart]['count'])



    with transaction.atomic():
        #创建事务保存点
        save_id = transaction.savepoint()

        #生成总订单逻辑
        user = User.objects.get(username=username)

        #生成订单号
        order_code = datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)

        order = Order.objects.create(
            uid = user.id,
            order_code = order_code,
            total_count = sum(cart_dict.values()),
            total_amount = 0,
            status = 1

        )

        #生成子订单

        totalcount = 0
        for gid,count in cart_dict.items():
            #判断库存
            good = Goods.objects.get(id = gid)

            if count > good.storenums:

                transaction.savepoint_rollback(save_id)
                return HttpResponse("库存不足")

            good.storenums -= count
            good.productnum += count
            good.save()

            order_detail = OrderDetail.objects.create(
                uid = user.id,
                order_code = order_code,
                goods_id = gid,
                counts = count,
                price = good.price
            )

            totalcount += count * good.price

            #清除redis中数据
            del cart_data[str(gid)]

        order.total_amount = totalcount

        #重新添加redis数据
        redis_cli.set(f'cart_{username}',json.dumps(cart_data))

        #提交事务
        transaction.savepoint_commit(save_id)

    return HttpResponse('订单生成成功')



