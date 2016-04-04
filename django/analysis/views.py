# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
# from analysis.models import Analysis

# Create your views here.
def index(request):
    """Top Page"""
    return render(request,
                  'analysis/index.html'
                  )
