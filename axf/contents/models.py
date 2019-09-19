from django.db import models

# Create your models here.


#基类模型
class Base(models.Model):
    img = models.CharField(max_length=255, verbose_name='图片信息')
    name = models.CharField(max_length=64, verbose_name='文字信息')

    class Meta:
        #不让模型映射为数据表
        abstract = True

#轮播图模型
class AxfWheel(Base):
    # img = models.CharField(max_length=255,verbose_name='图片信息')
    # name = models.CharField(max_length=64,verbose_name='文字信息')

    class Meta:
        db_table = 'axf_wheel'

#导航模型
class AxfNav(Base):
    # img = models.CharField(max_length=255, verbose_name='图片信息')
    # name = models.CharField(max_length=64, verbose_name='文字信息')

    class Meta:
        db_table = 'axf_nav'


#必买模型
class AxfMustbuy(Base):
    # img = models.CharField(max_length=255, verbose_name='图片信息')
    # name = models.CharField(max_length=64, verbose_name='文字信息')

    class Meta:
        db_table = 'axf_mustbuy'


#商店模型
class AxfShop(Base):
    # img = models.CharField(max_length=255, verbose_name='图片信息')
    # name = models.CharField(max_length=64, verbose_name='文字信息')

    class Meta:
        db_table = 'axf_shop'