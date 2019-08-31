from django.http import HttpRequest,HttpResponse,JsonResponse,HttpResponseBadRequest
from django.conf import settings
from user.models import User #导入数据库模型
import jwt
import datetime

def authenticate(view):
    def wrapper(request:HttpRequest):
        token = request.META.get('HTTP_JWT', None)
        if not token:
            return HttpResponseBadRequest('查无此人',status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(1,payload)
        except:
            return HttpResponseBadRequest('身份过期',status=401)
        try:
            user_id = payload.get('user_id', -1)
            user = User.objects.filter(pk = user_id).get()
            request.user = user
            print(2,'认证通过&&&&&&&&&&&&&&&&&&')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(status=401)
        ret = view(request)
        return ret
    return wrapper