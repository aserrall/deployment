from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q

from .forms import *
from .models import *


def index(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('forum')
    else:
        return render(request, 'likeme/HomeLanding.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('forum')  # TODO: Better make the user logout

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)

            password = form.cleaned_data.get('password')
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse("forum"))
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form, })


@login_required()
def forum(request):
    context = {}
    return render(request, 'likeme/foro.html', context)


@login_required()
def search_users(request):
    if request.method == "POST":
        if "buscarUsuari" in request.POST.keys():
            to_search = request.POST['buscarUsuari']
            try:
                users_found = User.objects.filter(first_name__icontains=to_search)
                request.session["to_search_friend"] = to_search

            except (KeyError, User.DoesNotExist, AttributeError):
                request.session["to_search_friend"] = "ERROR!"
                context = {'notfound': to_search,
                           'added': False}
                return render(request, 'search/SearchUser.html', context)

            pending_users = []
            print(users_found)
            for user in users_found:
                print(user)
                if user == request.user:
                    continue
                try:
                    f = FriendShip.objects.get(Q(user_sender=request.user, user_receiver=user, accepted=False) # Im okey fronted will deal with it
                                               | Q(user_sender=user, user_receiver=request.user, accepted=False))
                    if f is not None:
                        pending_users.append(f)

                except (KeyError, FriendShip.DoesNotExist, AttributeError):
                    print("error")

            print(pending_users)


            context = {'to_search': users_found}
            return render(request, 'search/SearchUser.html', context)

        elif "afegirUsuari" in request.POST.keys():
            to_add = request.POST['afegirUsuari']
            user_to_add = User.objects.get(first_name=to_add)

            context = {'to_search': user_to_add,
                       'added': True}
            return render(request, 'search/SearchUser.html', context)

    return render(request, 'search/SearchUser.html', {})


def mirarPerfil(request, email):
    try:
        u = User.objects.get(email=email)


        context = {
            'client': u}
    except:
        context = {}

    return render(request, 'likeme/perfil.html', context)
