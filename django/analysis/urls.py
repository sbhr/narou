# -*- coding: utf-8 -*-

from django.conf.urls import url
from analysis import views

urlpatterns = [
    # Top page
    url(r'^$', views.index, name='index'),
    url(r'^/ranking/$', views.ranking, name='ranking'),
]
