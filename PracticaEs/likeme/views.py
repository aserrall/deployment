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
def friends(request):
    # TODO: Here you are supposed to be able to handle friend requests and current friendships

    if request.method == 'GET':
        freq_current_friends = FriendShip.objects.filter(Q(user_sender=request.user, accepted=True) |
                                                         Q(user_receiver=request.user, accepted=True))
        freq_send = FriendShip.objects.filter(user_sender=request.user, accepted=False)
        freq_to_accept = FriendShip.objects.filter(user_receiver=request.user, accepted=False)

        context = {
            "freq_current_friends": freq_current_friends,
            "freq_send": freq_send,
            "freq_to_accept": freq_to_accept,
        }

        return render(request, 'likeme/friends.html', context)


@login_required()
def search_users(request):
    if request.method == "POST":
        if "buscarUsuari" in request.POST.keys():
            to_search = request.POST['buscarUsuari']
            try:
                users_found = User.objects.filter(first_name__icontains=to_search)  # TODO: Exclude yourself?
                request.session["to_search_friend"] = to_search

            except (KeyError, User.DoesNotExist, AttributeError):
                request.session["to_search_friend"] = "ERROR!"
                context = {'notfound': to_search,
                           'added': False}
                return render(request, 'search/SearchUser.html', context)

            pending_users = []
            print(users_found)
            for user in users_found:
                if user == request.user:
                    continue
                try:
                    f = FriendShip.objects.get(Q(user_sender=request.user, user_receiver=user,
                                                 accepted=False)  # Im okey fronted will deal with it
                                               | Q(user_sender=user, user_receiver=request.user, accepted=False))
                    if f is not None:
                        pending_users.append(f)

                except (KeyError, FriendShip.DoesNotExist, AttributeError):
                    print("error")

            print(pending_users)

            context = {'to_search': users_found}
            return render(request, 'search/SearchUser.html', context)

        elif "afegirUsuari" in request.POST.keys():
            user_to_add_email = request.POST['afegirUsuari']
            if user_to_add_email:
                try:
                    user_to_add = User.objects.get(email=user_to_add_email)
                    form = FriendSearchForm()
                    freq = form.save(commit=False)
                    freq.user_sender = request.user
                    freq.user_receiver = user_to_add
                    freq.save()
                    request.session['addResult'] = 'OK'
                except (KeyError, User.DoesNotExist, AttributeError):
                    request.session['addResult'] = 'ERROR!'

            context = {
                'to_search': [user_to_add],
                'added': True
            }

            return render(request, 'search/SearchUser.html', context)

        elif "refuseUsuari" in request.POST.keys():
            pass

        return HttpResponseRedirect(reverse("search_users"))

    elif request.method == "GET":
        pass
    return render(request, 'search/SearchUser.html', {})


def mirarPerfil(request, email):
    try:
        u = User.objects.get(email=email)

        context = {
            'client': u}
    except:
        context = {}

    return render(request, 'likeme/perfil.html', context)
