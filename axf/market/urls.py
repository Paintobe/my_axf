from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^market/(\d+)/(\d+)/(\d+)/$',views.index,name='index')
]