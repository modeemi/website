# -*- coding: utf-8 -*-

from .models import News
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class NewsForm(ModelForm):
    class Meta:
        model = News

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'news-form'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/uutiset/uusi/'
        self.helper.add_input(Submit('submit', 'Julkaise'))

        self.fields['title'].label = 'Otsikko'
        self.fields['text'].label = 'Uutisteksti'


class NewsUpdateForm(ModelForm):
    class Meta:
        model = News

    def __init__(self, *args, **kwargs):
        super(NewsUpdateForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')

        self.helper = FormHelper(self)
        self.helper.form_id = 'news-form'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/uutiset/' + str(instance.id) + '/muokkaa/'
        self.helper.add_input(Submit('submit', 'Päivitä'))

        self.fields['title'].label = 'Uusi otsikko'
        self.fields['text'].label = 'Uusi uutisteksti'
