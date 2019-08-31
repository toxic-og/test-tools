from django.conf.urls import url
from .views import reg, login, show

urlpatterns = [url(r'^reg$', reg),
               url(r'^login$', login),
               url(r'^show$', show)
               ]