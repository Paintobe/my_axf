from django.db import models

# Create your models here.

# typeid
# typename
# childtypenames
# typesort

#商品分类模型
class FoodType(models.Model):
    typeid = models.IntegerField(verbose_name='商品分类ID')
    typename = models.CharField(max_length=32,verbose_name='商品分类名称')
    childtypenames = models.CharField(max_length=255,verbose_name='子分类名称')
    typesort = models.IntegerField(verbose_name='排序')

    class Meta:
        db_table = 'axf_foodtype'

#商品模型
class Goods(models.Model):
    productid = models.IntegerField(verbose_name='商品ID')
    productimg = models.CharField(max_length=255,verbose_name='商品图片信息')
    productname = models.CharField(max_length=128,verbose_name='商品名称')
    productlongname = models.CharField(max_length=255,verbose_name='商品详细名称')
    specifics = models.CharField(max_length=64,verbose_name='商品规格')
    price = models.DecimalField(max_digits=6,decimal_places=2,verbose_name='商品价格')
    marketprice = models.DecimalField(max_digits=6,decimal_places=2,verbose_name='商品市场价格')
    categoryid = models.IntegerField(verbose_name='所属分类ID')
    childcid = models.IntegerField(verbose_name='所属子分类ID')
    childcidname = models.CharField(max_length=128,verbose_name='商品子分类名称')
    storenums = models.IntegerField(verbose_name='商品库存')
    productnum = models.IntegerField(verbose_name='商品销量')

    class Meta:
        db_table = 'axf_goods'