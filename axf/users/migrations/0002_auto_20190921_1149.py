# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-09-21 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='uploads', verbose_name='头像'),
        ),
    ]