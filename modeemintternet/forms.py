# -*- coding: utf-8 -*-

from modeemintternet.models import Application, News, Feedback
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ApplicationForm(ModelForm):
    password = forms.CharField(max_length=128, label='Haluamani salasana on')
    password_check = forms.CharField(max_length=128, label='Salasana uudelleen (tarkiste)')

    class Meta:
        model = Application
        exclude = ()

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


class NewsForm(ModelForm):
    class Meta:
        model = News
        exclude = ()

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
        exclude = ()

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
