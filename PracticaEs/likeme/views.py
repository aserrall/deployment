from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login
import datetime
from django.contrib.auth.decorators import login_required


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

            login(request, new_user)
            Client.objects.create(user=new_user, sexo=sex, dataAniversari=dAniversari, numTelefon=nTel)
            return HttpResponseRedirect(reverse("forum"))
    else:
        form = SignupForm()
    return render(request, "registration/register.html", {'form': form, })


@login_required()
def forum(request):
    context = {}
    return render(request, 'likeme/foro.html', context)


def mirarPerfil(request, user):
    
    u = User.objects.get(username = user)

    c = Client.objects.get(user=u)
    
    context = {
            'client' : c}

    return render(request, 'likeme/perfil.html', context)

