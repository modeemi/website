# -*- coding: utf-8 -*-

from .models import Application
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ApplicationForm(ModelForm):
    class Meta:
        model = Application

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'application-form'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/jaseneksi/hakemus/'
        self.helper.add_input(Submit('submit', 'Lähetä hakemus'))

        self.fields['email'].label = 'Sähköposti (ensisijaisesti tut.fi)'
        self.fields['first_name'].label = 'Etunimi'
        self.fields['last_name'].label = 'Sukunimi'
        self.fields['reason'].label = 'Peruste jäsenyyden hakemiselle'
        self.fields['primary_nick'].label = 'Haluamani käyttäjätunnus'
        self.fields['secondary_nick'].label = 'Jos on jo käytössä'
        self.fields['shell'].label = 'Haluamani komentokehoite'
        self.fields['funet_rules_accepted'].label = 'Hyväksyn FUNET:n käyttösäännöt'
        self.fields['funet_rules_accepted'].required = True

