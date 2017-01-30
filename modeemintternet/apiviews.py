# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import viewsets
from modeemintternet.models import News
from modeemintternet.serializers import NewsSerializer

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.order_by('-posted')
    serializer_class = NewsSerializer
