# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-09-21 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190921_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=50, verbose_name='邮箱'),
        ),
    ]
