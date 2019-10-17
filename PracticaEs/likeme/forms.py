from django import forms

from django.contrib.auth import authenticate, get_user_model
from django.db import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, FriendShip


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    sex = forms.ChoiceField(label='Sex', widget=forms.RadioSelect(), choices=[('1', 'Home'), ('2', 'Dona')])
    birth_date = forms.DateTimeField(label='Birth date', widget=forms.SelectDateWidget(years=list(range(1980, 2020))))
    phone_number = forms.CharField(label='Phone number')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'sex',
            'birth_date',
            'phone_number',
            'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email


class UserEditorForm(forms.ModelForm):
    email = forms.EmailField(label='Email address', required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    sex = forms.ChoiceField(label='Sex', required=True)
    birth_date = forms.DateTimeField(label='Birth date', required=True)
    phone_number = forms.CharField(label='Phone number', required=True)
    photo = forms.ImageField(label='Photo', required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'sex',
            'birth_date',
            'photo',
            'phone_number'
        ]


class FriendSearchForm(forms.ModelForm):
    class Meta:
        model = FriendShip
        fields = ["user_sender", "user_receiver"]