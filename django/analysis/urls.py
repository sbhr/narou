# -*- coding: utf-8 -*-

from django.conf.urls import url
from analysis import views

urlpatterns = [
    # Top page
    url(r'^$', views.index.index, name='index'),
    url(r'^about/$', views.about.about, name='about'),
    url(r'^ranking/$', views.ranking.ranking, name='ranking'),
    url(r'^ranking/list/(?P<term_id>\d+)$', views.RankingList.RankingList.as_view(), name='ranking_list'),
    url(r'^ranking/(?P<term_name>.+)$', views.ranking.ranking, name='ranking'),
    url(r'^search_letter/$', views.search_letter.search_letter, name='search_letter'),
    url(r'^search_title/$', views.search_title.search_title, name='search_title'),
    url(r'^detail_letter/(?P<value_letter>.+)&(?P<term_id>\d+)$', views.detail_letter.detail_letter, name='detail_letter'),
    url(r'^detail_title/(?P<title_id>\d+)$', views.detail_title.detail_title, name='detail_title'),
]
