# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.views.generic.list import ListView
from analysis.models import Score, Letter, Term
from analysis.forms import TermForm, SearchForm
from datetime import datetime

# Create your views here.
def index(request):
    """Top page"""

    #本日のランキング
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
    words = Letter.objects.filter(pos_id=2, term_id=3, date=raw_latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')[:10]
    for word in words:
        temp_word = word['value']
        word['related_novels'] = Score.objects.filter(term_id=3, date=raw_latest_date, title__name__contains=temp_word).select_related().all().order_by('rank')[:3]

    return render(request,
                  'analysis/index.html',
                  {'words': words})

# About page
def about(request):
    """About page"""

    return render(request,
                  'analysis/about.html')

# Ranking page
def ranking(request, term_name=u"総合"):
    """Ranking Page"""

    genre_list = [u"総合", u"文学", u"恋愛", u"歴史", u"推理", u"ファンタジー", u"SF", u"ホラー", u"コメディー", u"冒険", u"学園", u"戦記", u"童話", u"詩", u"エッセイ", u"その他"]
    selected_term = term_name
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
    target_terms = Term.objects.filter(name__contains=term_name).values('id', 'name')

    # Form
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['From']
            date_to   = form.cleaned_data['To']
        else:
            date_from = raw_latest_date
            date_to   = raw_latest_date
    else:
        form = TermForm()
        date_from = raw_latest_date
        date_to   = raw_latest_date

    # Get output data from database
    for term in target_terms:
        term['words'] = Letter.objects.filter(pos_id=2, term_id=int(term['id']), date__lte=date_to, date__gte=date_from).values('value').annotate(num_words=Count('value')).order_by('-num_words')[:10]
        term['num_datas'] = Score.objects.filter(term_id=int(term['id']), date__lte=date_to, date__gte=date_from).count()

    return render(request,
                  'analysis/ranking.html',
                  {'form':form,
                   'target_terms':target_terms,
                   'genre_list':genre_list,
                   'selected_term':selected_term})

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

# Search Title
def search_letter(request):
    """Search letter"""

    template_name='analysis/search_letter.html'
    paginate_by = 10
    target_terms = Term.objects.all()
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            _word = form.cleaned_data['word']
            _term = request.POST['term']

            words = Letter.objects.filter(term_id=_term, value__contains=_word).values('value').annotate(num_words=Count('value')).order_by('-num_words')

    else:
        form = SearchForm()
        words = ''

    return render(request,
                  'analysis/search_letter.html',
                  {'form':form,
                   'target_terms':target_terms,
                   'words':words})

# Search Title
def search_title(request):
    """Search title"""

    template_name='analysis/search_title.html'
    paginate_by = 10
