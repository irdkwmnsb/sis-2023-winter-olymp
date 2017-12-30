from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^initdb', views.initdb),
    url(r'^monitor', views.monitor),
]
