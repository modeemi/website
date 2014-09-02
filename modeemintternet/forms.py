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
        self.helper.form_action = '/jaseneksi/'
        self.helper.add_input(Submit('submit', 'Lähetä hakemus'))

        self.fields['email'].label = 'Sähköpostini on (ensisijaisesti tut.fi)'
        self.fields['first_name'].label = 'Etunimeni on'
        self.fields['last_name'].label = 'Sukunimeni on'
        self.fields['reason'].label = 'Peruste jäsenyyden hakemiselle, jos en ole opiskelija'
        self.fields['primary_nick'].label = 'Ensisijaisesti haluamani käyttäjätunnus on'
        self.fields['secondary_nick'].label = 'Vaihtoehto, jos ensisijainen on jo käytössä'
        self.fields['shell'].label = 'Haluamani komentokehoite kerhon *nix -koneilla'
        self.fields['funet_rules_accepted'].label = 'Hyväksyn <a href="http://www.csc.fi/hallinto/funet/esittely/etiikka/index_html">FUNET-verkon käyttösäännöt</a>'
        self.fields['funet_rules_accepted'].required = True

