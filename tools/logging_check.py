from django.http import JsonResponse
import jwt
from django.conf import settings
from blog.models import User


def logging_check(func):
    def wrap(request, *args, **kwargs):
        token = request.META.get('Authorization')
        if not token:
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        try:
            res = jwt.decode(token, settings.TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            print('jwt token error is {}'.format(e))
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        username = res['username']
        user = User.objects.get(Username=username)
        request.myuser = user

        return func(request, *args, **kwargs)

    return wrap
