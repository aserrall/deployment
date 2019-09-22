from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(forms.Form, UserCreationForm):
    anyN= ['1980','1981','1982','1983']
    Sexe = [('1', 'Home'), ('2', 'Dona')]
    choice = forms.ChoiceField(widget=forms.RadioSelect(), choices = Sexe)
    anyNeixement = forms.DateField(widget=forms.SelectDateWidget(years=anyN))
