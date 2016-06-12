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

# About page
def about(request):
    """About page"""

    return render(request,
                  'analysis/about.html')

# Ranking page
def ranking(request, term_name=u"総合"):
    """Ranking Page"""

    #var
    genre_list = [u"総合", u"文学", u"恋愛", u"歴史", u"推理", u"ファンタジー", u"SF", u"ホラー", u"コメディー", u"冒険", u"学園", u"戦記", u"童話", u"詩", u"エッセイ", u"その他"]
    selected_term = term_name
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
    target_terms = Term.objects.filter(name__contains=term_name).values('id', 'name')

    # Form
    if request.method == 'POST':
        form = TermForm(request.POST)

        # Validation
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

    # var
    context_object_name='words'
    template_name='analysis/ranking_list.html'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        # var
        raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
        # Get popular words
        words = Letter.objects.filter(pos_id=2, term_id=int(kwargs['term_id']), date=raw_latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')
        # add related title of novels
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

    # var
    target_terms = Term.objects.all()
    form = SearchLetterForm()

    # Form
    if request.method == 'POST':
        form = SearchLetterForm(request.POST)
        # Validation
        if form.is_valid():
            # var for search
            _word = form.cleaned_data['word']
            _term = request.POST['term']
            # Get Letters contain var for search
            letters = Letter.objects.filter(term_id=_term, value__contains=_word).values('value').annotate(num_letters=Count('value')).order_by('-num_letters')
            _term = int(_term)
    else:
        form = SearchLetterForm()
        letters = ''
        _term = ''

    return render(request,
                  'analysis/search_letter.html',
                  {'form':form,
                   'target_terms':target_terms,
                   'letters':letters,
                   'used_term':_term})

# Search Title
def search_title(request):
    """Search title"""

    # var
    paginate_by = 50
    form = SearchTitleForm
    query = request.GET.get('query')

    # Form
    if request.method == 'POST' or query is not None:
        # POST or Paging
        if query is None:
            form = SearchTitleForm(request.POST)
        else:
            form = SearchTitleForm({'word':query})
        if form.is_valid() or query is not None:
            # var for search
            _word = form.cleaned_data['word']
            # Get titles contain var for search
            title_list = Title.objects.filter(name__contains=_word).values('name','id')
            # encode long to int
            for row in title_list:
                row['id'] = int(row['id'])

            # Paging
            paginator = Paginator(title_list, paginate_by)
            page = request.GET.get('page')
            try:
                titles = paginator.page(page)
            except PageNotAnInteger:
                titles = paginator.page(1)
            except EmptyPage:
                titles = paginator.page(paginator.num_pages)

    else:
        form = SearchTitleForm()
        titles = ''
        _word = ''

    return render(request,
                  'analysis/search_title.html',
                  {'form':form,
                   'titles':titles,
                   'query':_word})

# Detail Letter
def detail_letter(request, value_letter, term_id):
    """Detail letter"""

    # var
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']

    # Get number of occurrences of value_letter in term of term_id
    dataset = Letter.objects.filter(value=value_letter, term_id=term_id).values('value', 'date').annotate(num_of_letters=Count('value')).values('date', 'num_of_letters')
    related_novels = Score.objects.filter(term_id=term_id, date=raw_latest_date, title__name__contains=value_letter).select_related().all().order_by('rank').distinct()[:10]

    return render(request,
                  'analysis/detail_letter.html',
                  {'value_letter':value_letter,
                   'term_id':term_id,
                   'dataset':dataset,
                   'related_novels':related_novels})

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
