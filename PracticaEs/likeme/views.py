from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from .forms import *
import datetime


def index(request):
    context = {}
    return render(request, 'likeme/HomeLanding.html', context)


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            
            new_user = form.save()
            dAniversari = datetime.date(
                    int(request.POST['anyNeixement_year']),
                    int(request.POST['anyNeixement_month']),
                    int(request.POST['anyNeixement_day']))
            sex = request.POST['choice']
            nTel = request.POST['n_tel']
            
            Client.objects.create(user=new_user, sexo = sex, dataAniversari = dAniversari, numTelefon=nTel)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = SignupForm()
    return render(request, "registration/register.html", {'form':form,})

def login_view(request):
    pass

def logout_view(request):
    pass

