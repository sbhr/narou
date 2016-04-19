# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.views.generic.list import ListView
from analysis.models import Score, Letter, Term
from datetime import datetime

# Create your views here.
def index(request):
    """Top Page"""

    #本日のランキング
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
    words = Letter.objects.filter(pos_id=2, term_id=3, date=raw_latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')[:10]
    for word in words:
        temp_word = word['value']
        word['related_novels'] = Score.objects.filter(term_id=3, date=raw_latest_date, title__name__contains=temp_word).select_related().all().order_by('rank')[:3]

    return render(request,
                  'analysis/index.html',
                  {'words': words})

# Ranking page
def ranking(request):
    """Ranking Page"""

    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
    terms = Term.objects.all().order_by('id')[:6].values('id', 'name')
    for term in terms:
        term['words'] = Letter.objects.filter(pos_id=2, term_id=int(term['id']), date=raw_latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')[:10]

    return render(request,
                  'analysis/ranking.html',
                  {'terms':terms})

# Ranking List
class RankingList(ListView):
    """Ranking List"""
    context_object_name='words'
    template_name='analysis/ranking_list.html'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
        words = Letter.objects.filter(pos_id=2, term_id=int(kwargs['term_id']), date=raw_latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')
        for (i, word) in enumerate(words):
                temp_word = word['value']
                word['id'] = i + 1
                word['related_novels'] = Score.objects.filter(term_id=int(kwargs['term_id']), date=raw_latest_date, title__name__contains=temp_word).select_related().all().order_by('rank')[:3]
        self.object_list = words

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)
