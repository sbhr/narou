# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime

# Form between Start day and End day on ranking.html
class TermForm(forms.Form):
    """Ranking page"""
    From = forms.DateField(initial=datetime.today())
    To = forms.DateField(initial=datetime.today())

# Form to search for letter
class SearchLetterForm(forms.Form):
    """Search Letter"""
    word = forms.CharField()
    term = forms.IntegerField()

# Form to search for title
class SearchTitleForm(forms.Form):
    """Search Title"""
    word = forms.CharField()
