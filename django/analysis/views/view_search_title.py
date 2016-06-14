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
