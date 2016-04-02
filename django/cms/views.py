# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView

from cms.models import Title, Score
from cms.forms import TitleForm, ScoreForm

# Create your views here.
def title_list(request):
    '''タイトルの一覧'''
    titles = Title.objects.all().order_by('id')
    return render(request,
                  'cms/title_list.html',    #使用するテンプレート
                  {'titles': titles})       #テンプレートに渡すデータ


def title_edit(request, title_id=None):
    '''タイトルの編集'''
    if title_id:
        # edit
        title = get_object_or_404(Title, pk=title_id)
    else:
        # add
        title = Title()

    if request.method == 'POST':
        form = TitleForm(request.POST, instance=title)
        if form.is_valid():
            title = form.save(commit=False)
            title.save()
            return redirect('cms:title_list')
    else:
        form = TitleForm(instance=title)

    return render(request, 'cms/title_edit.html', dict(form=form, title_id=title_id))


def title_del(request, title_id):
    '''タイトルの削除'''
    title = get_object_or_404(Title, pk=title_id)
    title.delete()
    return redirect('cms:title_list')


def score_edit(request, title_id, score_id=None):
    '''得点の編集'''
    title = get_object_or_404(Title, pk=title_id)
    if score_id:
        # edit
        score = get_object_or_404(Score, pk=score_id)
    else:
        # add
        score = Score()

    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)  #POSTされたrequestデータからフォームを作成
        if form.is_valid():
            score = form.save(commit=False)
            score.title = title
            title.save()
            return redirect('cms:score_list', title_id=title_id)
    else:
        form = ScoreForm(instance=score)    #scoreインスタンスからフォームを作成

    return render(request,
                  'cms/score_edit.html',
                  dict(form=form, title_id=title_id, score_id=score_id))


def score_del(request, title_id, score_id):
    '''得点の削除'''
    score = get_object_or_404(Score, pk=score_id)
    score.delete()
    return redirect('cms:score_list', title_id=title_id)


class ScoreList(ListView):
    '''得点の一覧'''
    context_object_name='scores'
    template_name='cms/score_list.html'
    paginate_by = 30 # 1ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        title = get_object_or_404(Title, pk=kwargs['title_id']) #親のタイトルを読む
        scores = title.scores_title.all().order_by('id')                #タイトルの子供の得点
        self.object_list = scores

        context = self.get_context_data(object_list=self.object_list, title=title)
        return self.render_to_response(context)
