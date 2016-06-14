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
# About page
def about(request):
    """About page"""

    return render(request,
                  'analysis/about.html')
