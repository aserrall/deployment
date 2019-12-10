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
    if request.method == 'POST':

        if "post_value" in request.POST:
            Posteig.objects.create(content=request.POST['content_post'], user_post=request.user)
        elif "comment_value" in request.POST:
            try:
                id = request.POST['comment_value']
                pr = Posteig.objects.get(id=id)
                Comments.objects.create(content=request.POST['content_comment-' + id], user_post=request.user,
                                        posteig_id=pr)
            except:
                pass
        elif "reply_value" in request.POST:
            try:
                id = request.POST['reply_value']
                c = Comments.objects.get(id=id)
                Reply.objects.create(content=request.POST['content_reply-'+id], user_post=request.user, posteig_id=c)
            except:
                pass
        elif "like_value" in request.POST:
            id = request.POST['like_value']
            try:
                pr = Posteig.objects.get(id=id)
                try:
                    liked = Like.objects.get(user_like=request.user, post_id=pr)
                    liked.delete()
                except (KeyError, Like.DoesNotExist, AttributeError):
                    Like.objects.create(post_id=pr, user_like=request.user)
            except:
                pass
        elif "delete_value" in request.POST:
            id = request.POST['delete_value']
            Posteig.objects.filter(id=id).delete()
        elif "deleteComment_value" in request.POST:
            id = request.POST['deleteComment_value']
            Comments.objects.filter(id=id).delete()
        elif "deleteReply_value" in request.POST:
            id = request.POST['deleteReply_value']
            Reply.objects.filter(id=id).delete()


    l = []

    freq_current_friends = FriendShip.objects.filter(Q(user_sender=request.user, accepted=True)
                                                    | Q(user_receiver=request.user, accepted=True))
    friends = [x.user_sender if x.user_sender != request.user else x.user_receiver for x in freq_current_friends]

    posts = Posteig.objects.filter(user_post__in=friends).exclude(user_post=request.user)

    # [ [P1, [(c,R)], L1 ], P2, PN]
    # [ (P1, [(C1,[R]), (C1,[R])] ) ]

    for p in posts:
        comments = Comments.objects.filter(posteig_id=p.id)
        likes = Like.objects.filter(post_id=p.id)
        user_likes = [x.user_like for x in likes]

        tr = [(q, Reply.objects.filter(posteig_id=q)) for q in comments]
        t = (p, tr, likes, user_likes)
        l.append(t)

    context = {
        'posts': l
    }
    return render(request, 'likeme/foro.html', context)


@login_required()
def friends(request):
    if request.method == "POST":
        if "cancel_freq" in request.POST.keys():
            freq_id = request.POST['cancel_freq']
            FriendShip.objects.get(id=freq_id).delete()
        elif "accept_freq" in request.POST.keys():
            freq_id = request.POST['accept_freq']
            FriendShip.objects.filter(id=freq_id).update(accepted=True)

        return HttpResponseRedirect(reverse("friends"))

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
        if "users_to_search" in request.POST.keys():
            to_search = request.POST['users_to_search']
            request.session["to_search_friend"] = to_search
            print(to_search)
        elif "send_freq" in request.POST.keys():
            user_to_add_email = request.POST['send_freq']
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

        elif "cancel_freq" in request.POST.keys():
            freq_id = request.POST['cancel_freq']
            FriendShip.objects.get(id=freq_id).delete()

        elif "accept_freq" in request.POST.keys():
            freq_id = request.POST['accept_freq']
            FriendShip.objects.filter(id=freq_id).update(accepted=True)

        return HttpResponseRedirect(reverse("search_users"))

    if request.method == "GET":
        to_search = request.session["to_search_friend"]
        # print(to_search)
        try:
            users_found = User.objects.filter(first_name__icontains=to_search).exclude(email=request.user.email)
            # print(users_found)
            l_freq_current_friends = []
            l_freq_send = []
            l_freq_to_accept = []
            l_possible_users = []

            for u in users_found:
                # print(u)
                freq_current_friends = FriendShip.objects.filter(
                    Q(user_sender=u, user_receiver=request.user, accepted=True) |
                    Q(user_sender=request.user, user_receiver=u, accepted=True))

                freq_send = FriendShip.objects.filter(user_sender=request.user, user_receiver=u,
                                                      accepted=False)

                freq_to_accept = FriendShip.objects.filter(user_sender=u, user_receiver=request.user,
                                                           accepted=False)
                # print(freq_current_friends)
                # print(freq_send)
                # print(freq_to_accept)

                if not freq_current_friends and not freq_send and not freq_to_accept:
                    l_possible_users.append(u)
                else:
                    if freq_current_friends:
                        l_freq_current_friends += freq_current_friends
                    if freq_send:
                        l_freq_send += freq_send
                    if freq_to_accept:
                        l_freq_to_accept += freq_to_accept

                # print(l_possible_users)
                # print(l_freq_to_accept)
                # print(l_freq_current_friends)
                # print(l_freq_send)

            context = {
                "l_freq_current_friends": l_freq_current_friends,
                "l_freq_send": l_freq_send,
                "l_freq_to_accept": l_freq_to_accept,
                "l_possible_users": l_possible_users
            }

            return render(request, 'search/SearchUser.html', context)

        except (KeyError, User.DoesNotExist, AttributeError):
            request.session["to_search_friend"] = "ERROR!"
            context = {'notfound': to_search}
            return render(request, 'search/SearchUser.html', context)


def mirarPerfil(request, email):
    if request.method == "POST":
        if "post_value" in request.POST:
            Posteig.objects.create(content=request.POST['content_post'], user_post=request.user)
        if "comment_value" in request.POST:
            try:
                id = request.POST['comment_value']
                pr = Posteig.objects.get(id=id)
                Comments.objects.create(content=request.POST['content_comment-' + id], user_post=request.user,
                                        posteig_id=pr)
            except:
                pass
        elif "reply_value" in request.POST:
            try:
                id = request.POST['reply_value']
                c = Comments.objects.get(id=id)
                Reply.objects.create(content=request.POST['content_reply-'+id], user_post=request.user, posteig_id=c)
            except:
                pass
        elif "like_value" in request.POST:
            id = request.POST['like_value']
            try:
                pr = Posteig.objects.get(id=id)
                try:
                    liked = Like.objects.get(user_like=request.user, post_id=pr)
                    liked.delete()
                except (KeyError, Like.DoesNotExist, AttributeError):
                    Like.objects.create(post_id=pr, user_like=request.user)
            except:
                pass
        elif "delete_value" in request.POST:
            id = request.POST['delete_value']
            Posteig.objects.filter(id=id).delete()
        elif "deleteComment_value" in request.POST:
            id = request.POST['deleteComment_value']
            Comments.objects.filter(id=id).delete()
        elif "deleteReply_value" in request.POST:
            id = request.POST['deleteReply_value']
            Reply.objects.filter(id=id).delete()
        elif "profile_status" in request.POST:
            u = LikeMeUser.objects.get(email=email)
            if u.profile_state == 1 and request.POST['profile_status']== "public":
                u.profile_state = 0
                u.save()
            elif u.profile_state == 0 and request.POST['profile_status']== "privat":
                u.profile_state = 1
                u.save()



    try:
        l = []
        u = User.objects.get(email=email)
        posts = Posteig.objects.filter(user_post=u).order_by('-creation_date')
        for p in posts:
            comments = Comments.objects.filter(posteig_id=p.id)
            likes = Like.objects.filter(post_id=p.id)
            user_likes = [x.user_like for x in likes]
            tr = [(q, Reply.objects.filter(posteig_id=q)) for q in comments]
            t = (p, tr, likes, user_likes)
            l.append(t)

        freq_current_friends = FriendShip.objects.filter(Q(user_sender=request.user, accepted=True)
                                                    | Q(user_receiver=request.user, accepted=True))
        friends = [x.user_sender if x.user_sender != request.user else x.user_receiver for x in freq_current_friends]
        
        aut = False

        u = LikeMeUser.objects.get(email=email)
        if u.profile_state == 0:
            aut = True
        elif u == request.user:
            aut = True
        elif u.profile_state == 1:
            if u in friends:
                aut = True
            else:
                aut = False

        if aut:
            context = {

                'client': u,
                'posts': l
            }
        else:
            context = {}
    except:
        context = {}

    return render(request, 'likeme/perfil.html', context)
