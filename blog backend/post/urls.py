from django.conf.urls import url
from .views import pub, get, getall

urlpatterns = [url(r'^put$', pub),
               url(r'^(\d+)$', get),
               url(r'^$', getall),
               ]