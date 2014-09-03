from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required

import os

from modeemintternet.views import render_with_context
from .models import News
from .forms import NewsForm, NewsUpdateForm

def read(request, pk=None):
    if pk:
        return render_with_context(request, 'read.html',
                {'news': News.objects.filter(id=pk)})
    return render_with_context(request, 'read.html',
            {'news': News.objects.order_by('-id')[:20]})

@permission_required('news.can_create', login_url='/login/')
def create(request):
    news_form = NewsForm()

    if request.POST:
        news_form = NewsForm(request.POST)

        if news_form.is_valid():
            news = news_form.save()
            news.set_poster(request)

    return render_with_context(request, 'create.html',
            {'form': news_form})

@permission_required('news.can_modify', login_url='/login/')
def update(request, pk):
    news_form = NewsUpdateForm(instance=News.objects.get(id=pk))

    if request.POST:
        news_form = NewsUpdateForm(request.POST, instance=News.objects.get(id=pk))

        if news_form.is_valid():
            news = news_form.save()
            news.set_modifier(request)

    return render_with_context(request, 'update.html',
            {'form': news_form})
