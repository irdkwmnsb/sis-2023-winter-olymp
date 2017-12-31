from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^statement/(?P<problem_id>\d+)$', views.read_statement, name='statement'),

    url(r'^monitor/(?P<contest_id>\d+)$', views.monitor),
    url(r'^monitor', views.monitor, name='monitor'),
]
