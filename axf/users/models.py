from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50,verbose_name='用户名')
    password = models.CharField(max_length=100,verbose_name='密码')
    phone = models.CharField(max_length=20,verbose_name='手机号')
    email = models.CharField(default='',max_length=50,verbose_name='邮箱')
    avatar = models.ImageField(upload_to='uploads',verbose_name='头像')
    is_active = models.BooleanField(default=0,verbose_name='激活状态')

    class Meta:
        db_table = 'axf_user'
