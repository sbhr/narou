# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
# About page
def about(request):
    """About page"""

    return render(request,
                  'analysis/about.html')
