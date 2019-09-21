from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse


def index(request):

    #判断用户是否登录
    if not request.session.get('username'):
        return redirect(reverse('users:login'))
    