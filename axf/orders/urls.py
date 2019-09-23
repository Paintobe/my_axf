from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^not_pay/$',views.not_pay,name='not_pay'),
    url(r'^order_pay/(\d+)/$',views.order_pay,name='order_pay')
]