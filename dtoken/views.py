import time
import jwt
from blog.models import User
from djangoProject import settings
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings


# Create your views here.
def tokens(request):  # api/login
    if request.method != 'POST':
        result = {'code': 0, 'msg': 'Please use post'}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    password = json_obj.get('password')
    if username is None or password is None:
        return JsonResponse({'code': 0, 'msg': '请求参数错误'})
    is_login = authenticate(request, username=username, password=password)
    if is_login is None:
        return JsonResponse({'code': 0, 'msg': '账号或密码错误'})
    login(request, is_login)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(is_login)
    token = jwt_encode_handler(payload)
    result = {'code': 1, 'msg': "login success!", 'data':
        {'token': token}}
    return JsonResponse(result)


def make_token(username, expire=3600 * 24):
    # 生成token
    now_t = time.time()
    payload = {'username': username, 'exp': now_t + expire}
    return jwt.encode(payload, settings.TOKEN_KEY, algorithm='HS256')
