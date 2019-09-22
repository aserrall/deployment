from django.shortcuts import render



def index(request):
    context = {}
    return render(request, 'likeme/HomeLanding.html', context)


def register(request):
    pass

def login_view(request):
    pass

def logout_view(request):
    pass

