# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-12 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='\u6587\u5b57')),
                ('date', models.DateTimeField(verbose_name='\u53ce\u96c6\u65e5\u6642')),
            ],
        ),
        migrations.CreateModel(
            name='Overview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_num_of_letter', models.IntegerField(verbose_name='\u30c7\u30fc\u30bf\u6570\uff08\u6587\u5b57/\u65e5\uff09')),
                ('daily_num_of_title', models.IntegerField(verbose_name='\u30c7\u30fc\u30bf\u6570\uff08\u30bf\u30a4\u30c8\u30eb/\u65e5\uff09')),
                ('total_num_of_letter', models.IntegerField(verbose_name='\u7d2f\u8a08\u30c7\u30fc\u30bf\u6570\uff08\u6587\u5b57\uff09')),
                ('total_num_of_title', models.IntegerField(verbose_name='\u7d2f\u8a08\u30c7\u30fc\u30bf\u6570\uff08\u30bf\u30a4\u30c8\u30eb\uff09')),
                ('date', models.DateTimeField(verbose_name='\u53ce\u96c6\u65e5\u6642')),
            ],
        ),
        migrations.CreateModel(
            name='Pos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=127, unique=True, verbose_name='\u7a2e\u985e')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(verbose_name='\u9806\u4f4d')),
                ('point', models.IntegerField(verbose_name='\u30dd\u30a4\u30f3\u30c8')),
                ('date', models.DateTimeField(verbose_name='\u53ce\u96c6\u65e5\u6642')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=127, unique=True, verbose_name='\u671f\u9593')),
                ('name', models.CharField(max_length=127, null=True, verbose_name='\u671f\u9593\u540d')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='\u30bf\u30a4\u30c8\u30eb')),
            ],
        ),
        migrations.AddField(
            model_name='score',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores_term', to='analysis.Term'),
        ),
        migrations.AddField(
            model_name='score',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores_title', to='analysis.Title'),
        ),
        migrations.AddField(
            model_name='letter',
            name='pos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letters_pos', to='analysis.Pos'),
        ),
        migrations.AddField(
            model_name='letter',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letters_term', to='analysis.Term'),
        ),
        migrations.AddField(
            model_name='letter',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letters_title', to='analysis.Title'),
        ),
    ]
