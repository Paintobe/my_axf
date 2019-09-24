import os

from celery import Celery

from worker import config

# 加载django的环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "axf.settings")

# 实例化celery
celery_app = Celery('axf_worker') #名字随意取

# 加载配置文件
celery_app.config_from_object(config)

# 自动注册任务
celery_app.autodiscover_tasks()