from django.shortcuts import *
from django.contrib.auth.models import User
from snsApp.models import *

# Create your views here.
def profile(request, username):
    # print(username)
    try:
        profile_user = Profile.objects.get(user = User.objects.get(username = username))
    except User.DoesNotExist:
        return redirect('/')
    # print(profile_user)
    # print(profile_user.picture)
    print(request.user.username)
    data = {'profile_user': profile_user,
            'username': username, 
            # 'picture': profile_user.picture.url,
            'num_of_playlists': profile_user.get_num_of_playlists(), 
            'num_of_followers': profile_user.get_num_of_follower(), 
            'num_of_following': profile_user.get_num_of_following(), 
            'music': '',
            'bio': profile_user.bio}
    if profile_user.music:
        data['music'] = f"{profile_user.music.title} - {profile_user.music.artist} "
    return render(request, 'profile.html', data)


def myprofile(request):
    if request.user.is_authenticated:
        return redirect('/'+request.user.username)
    else:
        #로그인하지않음
        return redirect('/login')