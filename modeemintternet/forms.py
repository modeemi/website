from django.forms import (
    Form,
    ModelForm,
    CharField,
    PasswordInput,
    EmailField,
    IntegerField,
)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from modeemintternet.models import Application, Feedback


class MembershipForm(Form):
    first_name = CharField(max_length=128, required=True)
    last_name = CharField(max_length=128, required=True)
    email = EmailField(max_length=128, required=True)
    municipality = CharField(max_length=128, required=False)


class MembershipFeeForm(Form):
    year = IntegerField(required=True)
    usernames = CharField(max_length=4096, required=True)


class PasswordForm(Form):
    password = CharField(
        max_length=256,
        label="Vanha salasana",
        widget=PasswordInput(),
    )
    new_password = CharField(
        min_length=12,
        max_length=256,
        label="Uusi salasana",
        widget=PasswordInput(),
    )
    new_password_check = CharField(
        min_length=12,
        max_length=256,
        label="Uusi salasana uudelleen",
        widget=PasswordInput(),
    )


class ApplicationForm(ModelForm):
    password = CharField(
        min_length=12,
        max_length=256,
        label="Salasana",
        widget=PasswordInput(),
    )
    password_check = CharField(
        min_length=12,
        max_length=256,
        label="Salasana uudelleen",
        widget=PasswordInput(),
    )

    class Meta:
        model = Application
        fields = (
            "first_name",
            "last_name",
            "email",
            "municipality",
            "username",
            "shell",
            "funet_rules_accepted",
            "virtual_key_required",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "application-form"
        self.helper.form_method = "POST"
        self.helper.form_action = "/jaseneksi/"
        self.helper.add_input(Submit("submit", "Lähetä hakemus"))

        self.fields["first_name"].label = "Etunimi"
        self.fields["last_name"].label = "Sukunimi"
        self.fields["email"].label = "Sähköpostiosoite"
        self.fields["municipality"].label = "Kotipaikka"

        self.fields["username"].label = "Käyttäjätunnus"
        self.fields["shell"].label = "Komentokehoite kerhon *nix -ympäristössä"
        self.fields["funet_rules_accepted"].label = "Hyväksyn Funet-verkon käyttöehdot"
        self.fields["funet_rules_accepted"].required = True
        self.fields[
            "virtual_key_required"
        ].label = "Tarvitsen virtuaaliavaimen kerhohuoneelle"


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "feedback-form"
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Lähetä"))

        self.fields["sender"].label = "Lähettäjä (vapaaehtoinen)"
        self.fields["email"].label = "Email (vapaaehtoinen)"
        self.fields["message"].label = "Palaute"
        self.fields["validation"].label = "Mikä on tämän kerhon nimi?"
        self.fields["validation"].required = True
