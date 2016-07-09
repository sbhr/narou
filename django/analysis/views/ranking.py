# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.db.models import Count
from analysis.models import Score, Letter, Term
from analysis.forms import TermForm

# Create your views here.
# Ranking page
def ranking(request, term_name=u"総合"):
    """Ranking Page"""

    #var
    genre_list = [u"総合", u"文学", u"恋愛", u"歴史", u"推理", u"ファンタジー", u"SF", u"ホラー", u"コメディー", u"冒険", u"学園", u"戦記", u"童話", u"詩", u"エッセイ", u"その他"]
    selected_term = term_name
    raw_latest_date = Score.objects.order_by('id').reverse()[:1].values('date')[0]['date']
    target_terms = Term.objects.filter(name__contains=term_name).values('id', 'name')

    # Form
    if request.method == 'POST':
        form = TermForm(request.POST)

        # Validation
        if form.is_valid():
            date_from = form.cleaned_data['From']
            date_to   = form.cleaned_data['To']
        else:
            date_from = raw_latest_date
            date_to   = raw_latest_date
    else:
        form = TermForm()
        date_from = raw_latest_date
        date_to   = raw_latest_date

    # Get output data from database
    for term in target_terms:
        term['words'] = Letter.objects.filter(pos_id=2, term_id=int(term['id']), date__lte=date_to, date__gte=date_from).values('value').annotate(num_words=Count('value')).order_by('-num_words')[:10]
        term['num_datas'] = Score.objects.filter(term_id=int(term['id']), date__lte=date_to, date__gte=date_from).count()

    return render(request,
                  'analysis/ranking.html',
                  {'form':form,
                   'target_terms':target_terms,
                   'genre_list':genre_list,
                   'selected_term':selected_term})
