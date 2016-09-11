# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Title(models.Model):
    # 小説のタイトル
    name = models.TextField('タイトル')


class Pos(models.Model):
    # 品詞の種類
    type = models.CharField('種類', max_length = 127, unique = True)

    def __unicode__(self):
        return self.type


class Term(models.Model):
    # 期間の種類
    type = models.CharField('期間', max_length = 127, unique = True)
    name = models.CharField('期間名', max_length = 127, null=True)

    def __str__(self):
        return self.type

    def __unicode__(self):
        return self.name


class Letter(models.Model):
    # 文字
    pos = models.ForeignKey(Pos, related_name='letters_pos')
    term = models.ForeignKey(Term, related_name='letters_term')
    title = models.ForeignKey(Title, related_name='letters_title')
    value = models.CharField('文字', max_length = 255)
    date = models.DateTimeField('収集日時')

    def __unicode__(self):
        return self.value


class Score(models.Model):
    # 得点や順位
    title = models.ForeignKey(Title, related_name='scores_title')
    term = models.ForeignKey(Term, related_name='scores_term')
    rank = models.IntegerField('順位')
    point = models.IntegerField('ポイント')
    date = models.DateTimeField('収集日時')


class Overview(models.Model):
    # データの概要
    daily_num_of_letter = models.IntegerField('データ数（文字/日）')
    daily_num_of_title = models.IntegerField('データ数（タイトル/日）')
    total_num_of_letter = models.IntegerField('累計データ数（文字）')
    total_num_of_title = models.IntegerField('累計データ数（タイトル）')
    date = models.DateTimeField('収集日時')
