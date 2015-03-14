# -*- coding: utf-8 -*-

from modeemintternet.models import Application, News, Feedback
from django.forms import ModelForm, CharField, PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ApplicationForm(ModelForm):
    password = CharField(max_length=128, label='Haluamani salasana on', widget=PasswordInput())
    password_check = CharField(max_length=128, label='Salasana uudelleen', widget=PasswordInput())

    class Meta:
        model = Application
        exclude = ('sha512', 'pbkdf2_sha256', 'application_accepted',
                'application_rejected', 'application_processed')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'application-form'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/jaseneksi/'
        self.helper.add_input(Submit('submit', 'Lähetä hakemus'))

        self.fields['email'].label = 'Sähköpostini on (ensisijaisesti tut.fi)'
        self.fields['first_name'].label = 'Etunimeni on'
        self.fields['last_name'].label = 'Sukunimeni on'
        self.fields['primary_nick'].label = 'Ensisijaisesti haluamani käyttäjätunnus on'
        self.fields['secondary_nick'].label = 'Vaihtoehto, jos ensisijainen on jo käytössä'
        self.fields['shell'].label = 'Haluamani komentokehoite kerhon *nix -koneilla'
        self.fields['funet_rules_accepted'].label = 'Hyväksyn FuNET-verkon käyttöehdot'
        self.fields['funet_rules_accepted'].required = True


class FeedbackForm(ModelForm):
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
