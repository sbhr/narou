# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime


class TermForm(forms.Form):
    """Ranking page"""
    From = forms.DateField(initial=datetime.today())
    To = forms.DateField(initial=datetime.today())

