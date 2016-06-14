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
def index(request):
    """Top page"""

    # var
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']

    # daily total rankig
    words = Letter.objects.filter(pos_id=2, term_id=3, date=raw_latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')[:10]
    # add related title of novels
    for word in words:
        temp_word = word['value']
        word['related_novels'] = Score.objects.filter(term_id=3, date=raw_latest_date, title__name__contains=temp_word).select_related().all().order_by('rank')[:3]

    # Lateset Overview of Data
    overview = Overview.objects.all().order_by('-id')[:1]

    # Overview graph
    dataset = Overview.objects.all()

    return render(request,
                  'analysis/index.html',
                  {'words': words,
                   'overview':overview,
                   'dataset':dataset})
