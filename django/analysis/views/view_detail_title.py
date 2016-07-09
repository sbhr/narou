# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.db.models import Count
from analysis.models import Score, Title
from janome.tokenizer import Tokenizer

# Create your views here.
# Detail Title
def detail_title(request, title_id):
    """Detail title"""

    # var
    dict_for_rank = {}
    dict_for_point = {}
    graph_data_rank = []
    graph_data_point = []
    array_for_tokens = []

    # Get name of title_id
    name_of_title = Title.objects.filter(id=title_id).values('name')[0]['name']
    # Get term_ids of title_id
    all_listed_term = Score.objects.filter(title_id=title_id).select_related().values('term_id', 'term__name').distinct()
    all_listed_date = Score.objects.filter(title_id=title_id).values('date').distinct()

    # Get Score of title_id in all of the term
    scoreset = Score.objects.filter(title_id=title_id).select_related().values('title__name', 'term__name', 'rank', 'point', 'date')

    # Fill dict_for_rank with 0
    for i in xrange(0, len(all_listed_term)):
        dict_for_rank[all_listed_term[i]['term__name']] = {}
        dict_for_point[all_listed_term[i]['term__name']] = {}
        for j in xrange(0, len(all_listed_date)):
            dict_for_rank[all_listed_term[i]['term__name']][all_listed_date[j]['date']] = "NaN"
            dict_for_point[all_listed_term[i]['term__name']][all_listed_date[j]['date']] = "NaN"

    # Assign the data of rank
    for row in scoreset:
        dict_for_rank[row['term__name']][row['date']] = row['rank']
        dict_for_point[row['term__name']][row['date']] = row['point']

    # Format tha dataset for Google chart
    for i in xrange(-1, len(all_listed_date)):
        # at the first loop
        if i == -1:
            tmp = []
            tmp.append('date')
            for j in xrange(0, len(all_listed_term)):
                tmp.append(all_listed_term[j]['term__name'])
            graph_data_rank.append(tmp)
            graph_data_point.append(tmp)
        else:
            tmp_rank = []
            tmp_point = []
            tmp_rank.append(all_listed_date[i]['date'])
            tmp_point.append(all_listed_date[i]['date'])
            for j in xrange(0, len(all_listed_term)):
                tmp_rank.append(dict_for_rank[all_listed_term[j]['term__name']][all_listed_date[i]['date']])
                tmp_point.append(dict_for_point[all_listed_term[j]['term__name']][all_listed_date[i]['date']])
            graph_data_rank.append(tmp_rank)
            graph_data_point.append(tmp_point)

    # Analysis title
    t = Tokenizer()
    tokens = t.tokenize(name_of_title)
    for token in tokens:
        temp = {
            'surface':  token.surface,
            'pos':  token.part_of_speech.split(',')[0]
        }
        array_for_tokens.append(temp)

    return render(request,
                  'analysis/detail_title.html',
                  {'name_of_title':name_of_title,
                   'graph_data_rank':graph_data_rank,
                   'graph_data_point':graph_data_point,
                   'array_for_tokens':array_for_tokens})
