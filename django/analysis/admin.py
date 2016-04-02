# -*- coding: utf-8 -*-

from django.contrib import admin
from cms.models import Title, Term, Pos, Letter, Score

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
    list_display = ('id', 'type',)
    list_display_links = ('type',)
admin.site.register(Term, TermAdmin)


class LetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos', 'term', 'value', 'date',)
    list_display_links = ('value',)
admin.site.register(Letter, LetterAdmin)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'term', 'rank', 'point', 'date',)
    list_display_links = ('rank', 'point',)
admin.site.register(Score, ScoreAdmin)
