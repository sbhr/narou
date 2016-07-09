# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.db.models import Count
from django.views.generic.list import ListView
from analysis.models import Score, Letter

# Create your views here.
# Ranking List
class RankingList(ListView):
    """Ranking List"""

    # var
    context_object_name='words'
    template_name='analysis/ranking_list.html'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        # var
        raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
        # Get popular words
        words = Letter.objects.filter(pos_id=2, term_id=int(kwargs['term_id']), date=raw_latest_date).values('value').annotate(num_words=Count('value')).order_by('-num_words')
        # add related title of novels
        for (i, word) in enumerate(words):
                temp_word = word['value']
                word['id'] = i + 1
                word['related_novels'] = Score.objects.filter(term_id=int(kwargs['term_id']), date=raw_latest_date, title__name__contains=temp_word).select_related().all().order_by('rank')[:3]

        self.object_list = words
        context = self.get_context_data(object_list=self.object_list)

        return self.render_to_response(context)
