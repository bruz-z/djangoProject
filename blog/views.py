import hashlib
import json

from django.utils.decorators import method_decorator

from .models import *
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from tools.logging_check import logging_check


@logging_check
def users_views(request, username):
    if request.method != 'POST':
        result = {'code': 10102, 'error': 'use POST！'}
        return JsonResponse(result)
    user = request.myuser
    avatar = request.FILES['avatar']
    user.avatar = avatar
    user.save()
    return JsonResponse({'code': 200})


class UserViews(View):
    def get(self, request, username=None):
        if username:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                result = {'code': 10101, 'error': '用户名不存在！'}
                return JsonResponse(result)
            result = {'code': 200, 'username': username,
                      'data': {'nickname': user.nickname, 'email': user.email, 'sign': user.sign,
                               'info': user.info, 'avatar': str(user.avatar)}}
            return JsonResponse(result)

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj.get('email')
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        phone = json_obj.get('phone')
        old_user = UserProfile.objects.filter(username=username)
        if password_1 != password_2:
            result = {'code': 10100, 'error': '密码不一致!'}
            return JsonResponse(result)
        if old_user:
            result = {'code': 10105, 'error': '用户名已存在!'}
            return JsonResponse(result)
        p_m = hashlib.md5()
        p_m.update(password_1.encode())
        # 创建用户
        try:
            UserProfile.objects.create(username=username, password=p_m.hexdigest(),
                                       nickname=username, email=email)
        except Exception as e:
            print(e)
            result = {'code': 10106, 'error': 'error!'}
            return JsonResponse(result)

        result = {'code': 200, 'username': username, 'data': {}}
        return JsonResponse(result)

    @method_decorator(logging_check)
    def put(self, request, username=None):
        json_str = request.body
        json_obj = json.loads(json_str)
        user = request.myuser
        user.sign = json_obj['sign']
        user.info = json_obj['info']
        user.nickname = json_obj['nickname']
        user.save()
        return JsonResponse({'code': 200})
