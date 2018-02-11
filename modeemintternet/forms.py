# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from modeemintternet.models import Application, Feedback
from django.forms import ModelForm, CharField, PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class ApplicationForm(ModelForm):
    password = CharField(max_length=128, label='Haluamani salasana on', widget=PasswordInput())
    password_check = CharField(max_length=128, label='Salasana uudelleen', widget=PasswordInput())
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        model = Application
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'shell',
            'funet_rules_accepted',
            'virtual_key_required',
        )

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'application-form'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/jaseneksi/'
        self.helper.add_input(Submit('submit', 'Lähetä hakemus'))

        self.fields['email'].label = 'Sähköpostini on'
        self.fields['first_name'].label = 'Etunimeni on'
        self.fields['last_name'].label = 'Sukunimeni on'
        self.fields['username'].label = 'Haluamani käyttäjätunnus on'
        self.fields['shell'].label = 'Haluamani komentokehoite kerhon *nix -koneilla'
        self.fields['funet_rules_accepted'].label = 'Hyväksyn FuNET-verkon käyttöehdot'
        self.fields['funet_rules_accepted'].required = True
        self.fields['virtual_key_required'].label = 'Tarvitsen virtuaaliavaimen kerhohuoneelle'


class FeedbackForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        model = Feedback
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')

        self.helper = FormHelper(self)
        self.helper.form_id = 'feedback-form'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Lähetä'))

        self.fields['sender'].label = 'Lähettäjä (vapaaehtoinen)'
        self.fields['email'].label = 'Email (vapaaehtoinen)'
        self.fields['message'].label = 'Palaute'
