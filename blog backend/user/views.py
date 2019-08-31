from django.shortcuts import render
from django.conf import settings
from django.http import HttpRequest,JsonResponse,HttpResponseBadRequest
import simplejson
from .models import User #导入数据库模型
import jwt
import bcrypt
import datetime

AUTH_EXPIRE = 8*60*60
def gen_token(user_id):
    return jwt.encode({
        'user_id':user_id,
        'exp':int(datetime.datetime.now().timestamp() + AUTH_EXPIRE)
    },settings.SECRET_KEY, 'HS256').decode()

def reg(request:HttpRequest):
    print(1,request.POST)
    print(2,request.body)
    payload = simplejson.loads(request.body)
    try:
        email = payload['email']
        query = User.objects.filter(email=email)
        print(3,query)
        print(4,type(query), query.query)
        if query.first():
            return HttpResponseBadRequest('用户名已存在----',status=401)
        name = payload['name']
        passwd = bcrypt.hashpw(payload['passwd'].encode(), bcrypt.gensalt())
        print(5,email, passwd, name)

        user = User()
        user.name = name
        user.passwd = passwd
        user.email = email

        try:
            user.save()
            return JsonResponse({'token':gen_token(user.id)})
        except:
            raise
    except Exception as e:
        print(6,e)
        return HttpResponseBadRequest('用户名已存在',status=402)


def login(request:HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        email = payload['email']
        user = User.objects.filter(email = email).get()

        print(payload['passwd'])
        print(user.passwd)

        if bcrypt.checkpw(payload['passwd'].encode(), user.passwd.encode()):
            token = gen_token(user.id)
            print(3,token)
            res = JsonResponse({
                'user' : {
                    'user_id' : user.id,
                    'name' : user.name,
                    'email' : user.email
                },
                'token' : token
            })
            coo = res.set_cookie('jwt', token)
            print(4,coo)
            return res
        else:
            return HttpResponseBadRequest('登录失败')
    except Exception as e:
        return HttpResponseBadRequest('登录失败')

def show(request:HttpRequest):
    meta = request.META
    #print(meta)
    #print(list(filter(lambda x: x.lower().endswith('jwt'),meta)))
    print(meta['HTTP_JWT'])

    return JsonResponse({})