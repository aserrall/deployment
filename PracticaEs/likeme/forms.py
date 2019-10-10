from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import FriendShip


class SignupForm(forms.Form, UserCreationForm):
    anyN = ['1980', '1981', '1982', '1983']
    Sexe = [('1', 'Home'), ('2', 'Dona')]
    choice = forms.ChoiceField(widget=forms.RadioSelect(), choices=Sexe)
    anyNeixement = forms.DateField(widget=forms.SelectDateWidget(years=anyN))


class FriendSearchForm(forms.ModelForm):
    class Meta:
        model = FriendShip
        fields = ["user_sender", "user_receiver"]