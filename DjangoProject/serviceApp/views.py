from django.shortcuts import *
import snsApp.views
from django.contrib.auth.models import User
from django.contrib import auth

from snsApp.models import *
from playlistApp.models import *

import CrawlPlaylist

chromedriverpath = 'C:\chromedriver.exe'


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

def integrate(request):
    return render(request, 'integrate.html')

    
def add_integrate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            msa = MusicServiceAccount(user=request.user.profile, music_provider=1, username=request.POST['username'], password=request.POST['password'])
            print(request.POST['provider'])
            msa.music_provider = msa.get_provider_from_val(request.POST['provider'])
            print( msa.get_provider_from_val(request.POST['provider']))
            msa.save()

            return redirect('/myprofile')
        else:
            return render(request, 'addintegrate.html')
    else:
        return redirect('/login')


def crawl(request):
    if request.user.is_authenticated:
        msa = request.user.profile.primaryMusicAccount
        Playlist()

        mypl = CrawlPlaylist.PlaylistManager(chromedriverpath)
        ui = CrawlPlaylist.UserInfo(msa.music_provider-1, 'local', msa.username, msa.password)
        mypl.login(ui)
        playlist_list = mypl.crawl(ui)

        print(playlist_list)

        for playlist in playlist_list:
            this_pl = Playlist()
            this_pl.title = playlist.name
            this_pl.writer = request.user
            this_pl.save()

            i = 0
            for music in playlist.music_list:
                print(music.name)
                print(music.melonUID)
                try:
                    this_music = Song.objects.get(melonUid=music.melonUID)
                    
                except:
                    this_music = Song()
                    this_music.title = music.name
                    this_music.artist = music.artist
                    this_music.album = music.album
                    this_music.melonUid = music.melonUID
                    # this_music.melonUid = UIDs[0]
                    # this_music.genieUid = 0
                    # this_music.floUid = 0
                    # this_music.viveUid = 0
                    # this_music.time = 0
                    this_music.save()
                relationship = Relationship()
                relationship.index = i
                relationship.playlistObj = this_pl
                relationship.songObj = this_music
                relationship.save()
                i += 1

        del mypl

        return redirect('/myprofile')
    else:
        return redirect('/login')