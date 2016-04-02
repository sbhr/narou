# -*- coding: utf-8 -*-

from django.conf.urls import url
from cms import views

urlpatterns = [
    # タイトル
    url(r'^title/$', views.title_list, name = 'title_list'),
    url(r'^title/add/$', views.title_edit, name = 'title_add'),
    url(r'^title/mod/(?P<title_id>\d+)/$', views.title_edit, name = 'title_mod'),
    url(r'^title/del/(?P<title_id>\d+)/$', views.title_del, name = 'title_del'),
    #得点
    url(r'^score/(?P<title_id>\d+)/$', views.ScoreList.as_view(), name='score_list'),
    url(r'^score/add/(?P<title_id>\d+)/$', views.score_edit, name='score_add'),
    url(r'^score/mod/(?P<title_id>\d+)/(?P<score_id>\d+)/$', views.score_edit, name='score_mod'),
    url(r'^score/del/(?P<title_id>\d+)/(?P<score_id>\d+)/$', views.score_del, name='score_del'),
]
