# -*- coding: utf-8 -*-

from django.contrib import admin
from analysis.models import Title, Term, Pos, Letter, Score, Overview

# Register your models here.
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)
admin.site.register(Title, TitleAdmin)


class PosAdmin(admin.ModelAdmin):
    list_display = ('id', 'type',)
    list_display_links = ('type',)
admin.site.register(Pos, PosAdmin)


class TermAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name',)
    list_display_links = ('type', 'name',)
admin.site.register(Term, TermAdmin)


class LetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos', 'term', 'value', 'date',)
    list_display_links = ('value',)
admin.site.register(Letter, LetterAdmin)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'term', 'rank', 'point', 'date',)
    list_display_links = ('rank', 'point',)
admin.site.register(Score, ScoreAdmin)


class OverviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'daily_num_of_letter', 'daily_num_of_title', 'total_num_of_letter', 'total_num_of_title', 'date')
    list_display_links = ('daily_num_of_letter', 'daily_num_of_title', 'total_num_of_letter', 'total_num_of_title')
admin.site.register(Overview, OverviewAdmin)
