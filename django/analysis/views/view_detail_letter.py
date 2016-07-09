# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.db.models import Count
from analysis.models import Score, Letter

# Create your views here.
# Detail Letter
def detail_letter(request, value_letter, term_id):
    """Detail letter"""

    # var
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']

    # Get number of occurrences of value_letter in term of term_id
    dataset = Letter.objects.filter(value=value_letter, term_id=term_id).values('value', 'date').annotate(num_of_letters=Count('value')).values('date', 'num_of_letters')
    related_novels = Score.objects.filter(term_id=term_id, date=raw_latest_date, title__name__contains=value_letter).select_related().all().order_by('rank').distinct()[:10]

    return render(request,
                  'analysis/detail_letter.html',
                  {'value_letter':value_letter,
                   'term_id':term_id,
                   'dataset':dataset,
                   'related_novels':related_novels})
