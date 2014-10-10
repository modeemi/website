# -*- coding: utf-8 -*-

from rest_framework import serializers
from modeemintternet.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News