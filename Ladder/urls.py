from django.urls import path, re_path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        re_path('ladder/(?P<cfHandle>[A-Za-z0-9]+)/$', views.home, name='home'),
        re_path('ladder/(?P<cfHandle>[A-Za-z0-9]+)/(?P<category>[-\w]+)/$', views.ladder, name='ladder'),
]
