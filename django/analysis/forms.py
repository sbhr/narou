# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime


class TermForm(forms.Form):
    """Ranking page"""
    From = forms.DateField(initial=datetime.today())
    To = forms.DateField(initial=datetime.today())


class SearchLetterForm(forms.Form):
    """Search Letter"""
    word = forms.CharField()
    term = forms.IntegerField()


class SearchTitleForm(forms.Form):
    """Search Title"""
    word = forms.CharField()
