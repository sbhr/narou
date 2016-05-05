# -*- coding: utf-8 -*-

from django.conf.urls import url
from analysis import views

urlpatterns = [
    # Top page
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^ranking/$', views.ranking, name='ranking'),
    url(r'^ranking/list/(?P<term_id>\d+)$', views.RankingList.as_view(), name='ranking_list'),
    url(r'^ranking/(?P<term_name>.+)$', views.ranking, name='ranking'),
]
