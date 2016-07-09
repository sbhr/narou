# -*- coding: utf-8 -*-

from django.conf.urls import url
from analysis import views

urlpatterns = [
    # Top page
    url(r'^$', views.view_index.index, name='index'),
    url(r'^about/$', views.view_about.about, name='about'),
    url(r'^ranking/$', views.view_ranking.ranking, name='ranking'),
    url(r'^ranking/list/(?P<term_id>\d+)$', views.view_RankingList.RankingList.as_view(), name='ranking_list'),
    url(r'^ranking/(?P<term_name>.+)$', views.view_ranking.ranking, name='ranking'),
    url(r'^search_letter/$', views.view_search_letter.search_letter, name='search_letter'),
    url(r'^search_title/$', views.view_search_title.search_title, name='search_title'),
    url(r'^detail_letter/(?P<value_letter>.+)&(?P<term_id>\d+)$', views.view_detail_letter.detail_letter, name='detail_letter'),
    url(r'^detail_title/(?P<title_id>\d+)$', views.view_detail_title.detail_title, name='detail_title'),
]
