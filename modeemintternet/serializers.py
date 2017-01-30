# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers
from modeemintternet.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
