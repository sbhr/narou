# -*- coding: utf-8 -*-

from django.forms import ModelForm
from cms.models import Title, Score


class TitleForm(ModelForm):
    '''タイトルのフォーム'''
    class Meta:
        model = Title
        fields = ('name', )


class ScoreForm(ModelForm):
    '''得点のフォーム'''
    class Meta:
        model = Score
        fields = ('rank', )
