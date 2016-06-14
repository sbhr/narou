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
