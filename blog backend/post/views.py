from django.http import HttpResponseBadRequest, HttpRequest, JsonResponse, HttpResponseNotFound
from tool.wrapper import authenticate
from user.models import User
from .models import Post, Content
import simplejson, datetime, math
from tool.validate import validate
# Create your views here.

@authenticate
def pub(request:HttpRequest):
    post = Post()
    content = Content()
    try:
        payload = simplejson.loads(request.body)
        print(1,payload)
        post.title = payload['title']
        #post.author = request.user
        post.author = User(id=request.user.id)
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.save()

        cont = payload['content']
        content.post = post
        content.content = cont
        content.save()
        return JsonResponse({
            'post_id':post.id
        })
    except Exception as e:
        print(2,e)
        return HttpResponseBadRequest('发布失败',status=407)

def get(request:HttpRequest, id):
    try:
        id = int(id)
        print(1,id)
        post = Post.objects.get(pk=id)
        print(2,post)
        if post:
            return JsonResponse({
                'post':{
                    'post_id':post.id,
                    'title':post.title,
                    'author':post.author.name,
                    'author_id':post.author.id,
                    'postdate':post.postdate.timestamp(),
                    'content':post.content.content
                }
            })
    except Exception as e:
        print(3,e)
        return HttpResponseNotFound('文章不存在')

def getall(request:HttpRequest):
    page = validate(request.GET, 'page', int, 1, lambda x,default :x if x>0 else default)
    size = validate(request.GET, 'size', int, 20, lambda x, y:x if x>0 and x<101 else y)
    # try:
    #     page = int(request.GET.get('page',1))
    #     page = page if page>0 else 1
    # except:
    #     page = 1
    # try:
    #     size = int(request.GET.get('size',20))
    #     size = size if size>0 and size<101 else 20
    # except:
    #     size = 20
    try:
        start = (page-1)*size
        posts = Post.objects.order_by('-id')
        print(1,posts.query)
        count = posts.count()
        posts = posts[start:start+size]
        print(2,posts.query)
        return JsonResponse({
            'posts':[{
                'post_id':post.id,
                'title':post.title
            }for post in posts],
            'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages':math.ceil(count/size)
            }
        })

    except Exception as e:
        print(e)
        return HttpResponseBadRequest('无数据')





