# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from analysis.models import Score, Letter
from datetime import datetime

# Create your views here.
def index(request):
    """Top Page"""

    #本日のランキング
    latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
    words = Letter.objects.filter(pos_id=2, term_id=3, date=latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')[:10]
    for word in words:
        temp_word = word['value']
        word['related_novels'] = Score.objects.filter(term_id=3, date=latest_date, title__name__contains=temp_word).select_related().all().order_by('rank')[:1]
    return render(request,
                  'analysis/index.html',
                  {'latest_date': latest_date, 'words': words})
