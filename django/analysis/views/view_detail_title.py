# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from analysis.models import Score, Letter, Term, Title, Overview
from analysis.forms import TermForm, SearchLetterForm, SearchTitleForm
from datetime import datetime

# Create your views here.
# Detail Title
def detail_title(request, title_id):
    """Detail title"""

    # var
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']

    # Get name of title_id
    name_of_title = Title.objects.filter(id=title_id).values('name')[0]['name']
    # Get term_ids of title_id
    all_listed_term = Score.objects.filter(title_id=title_id).select_related().values('term_id', 'term__name').distinct()
    all_listed_date = Score.objects.filter(title_id=title_id).values('date').distinct()

    # Get Score of title_id in all of the term
    scoreset = Score.objects.filter(title_id=title_id).select_related().values('title__name', 'term__name', 'rank', 'point', 'date')

    temp = {}
    graph_data = []

    for i in xrange(0, len(all_listed_term)):
        temp[all_listed_term[i]['term__name']] = {}
        for j in xrange(0, len(all_listed_date)):
            temp[all_listed_term[i]['term__name']][all_listed_date[j]['date']] = 0
    for row in scoreset:
        temp[row['term__name']][row['date']] = row['rank']
    for i in xrange(-1, len(all_listed_date)):
        if i == -1:
            tmp = []
            tmp.append('date')
            for j in xrange(0, len(all_listed_term)):
                tmp.append(all_listed_term[j]['term__name'])
            graph_data.append(tmp)
        else:
            tmp = []
            tmp.append(all_listed_date[i]['date'])
            for j in xrange(0, len(all_listed_term)):
                tmp.append(temp[all_listed_term[j]['term__name']][all_listed_date[i]['date']])
            graph_data.append(tmp)


    # Get number of occurrences of title_id in term of term_id
    # dataset = Title.objects.filter(value=value_letter, term_id=term_id).values('value', 'date').annotate(num_of_letters=Count('value')).values('date', 'num_of_letters')
    # related_novels = Score.objects.filter(term_id=term_id, date=raw_latest_date, title__name__contains=value_letter).select_related().all().order_by('rank').distinct()[:10]

    return render(request,
                  'analysis/detail_title.html',
                  {'name_of_title':name_of_title,
                   'graph_data':graph_data})
