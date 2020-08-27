from django.shortcuts import *
import snsApp.views
from django.contrib.auth.models import User
from django.contrib import auth

from snsApp.models import *

# Create your views here.
# def root(request, query):
#     if query == 'home':
#         return home(request)
#     elif query == 'feeds':
#         return feeds(request)
#     elif query == 'popular':
#         return popular(request)
#     else:
#         return snsApp.views.profile(request, query)


def home(request):
    return render(request, 'home.html')


def feeds(request):
    return render(request, 'home.html')


def popular(request):
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('/'+request.user.username)
    else:
        #로그인하지않음
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/myprofile')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
            

def register(request):
    if request.user.is_authenticated:
        return redirect('/'+request.user.username)
    else:
        #로그인하지않음
        if request.method == "POST":
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, user)
            return redirect('/integrate')
        else:
            return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def add_integrate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            msa = MusicServiceAccount(user=request.user.profile, music_provider=1, username=request.POST['username'], password=request.POST['password'])
            print(request.POST['provider'])
            msa.music_provider = msa.get_provider_from_val(request.POST['provider'])
            print( msa.get_provider_from_val(request.POST['provider']))
            msa.save()


            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, user)
            return redirect('/integrate')
        else:
            return render(request, 'addintegrate.html')
    else:
        return redirect('/login')