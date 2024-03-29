# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-09-22 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='用户id')),
                ('order_code', models.CharField(max_length=100, verbose_name='订单编号')),
                ('total_count', models.IntegerField(verbose_name='订单总数量')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='订单总金额')),
                ('status', models.SmallIntegerField(verbose_name='1为未支付，2为未发货，3为未收货')),
            ],
            options={
                'db_table': 'axf_order',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='用户id')),
                ('order_code', models.CharField(max_length=100, verbose_name='订单编号')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('counts', models.IntegerField(verbose_name='商品数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='商品单价')),
            ],
            options={
                'db_table': 'axf_order_detail',
            },
        ),
    ]
