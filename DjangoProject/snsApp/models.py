from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from playlistApp.models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True) #자기소개
    picture = models.ImageField(blank = True, upload_to = 'playlistProfile/', null=True, default=None) #프로필사진
    music = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, default=None, blank=True) #프로필뮤직
    primaryMusicAccount = models.ForeignKey('MusicServiceAccount', on_delete=models.SET_NULL, default=None, null=True, blank=True) #담기할때 연결되는 음원서비스계정
    follow = models.ManyToManyField(User, related_name='follow', blank=True) #팔로잉하는 유저들

    def __str__(self):
        return f"{self.user.username} / {self.primaryMusicAccount} / 소유 플레이리스트: {self.get_num_of_playlists()}/ 팔로우: {self.get_num_of_following()} / 팔로워: {self.get_num_of_follower()} / 프로필음악: {self.music}"

    #팔로잉 수 반환
    def get_num_of_following(self):
        return len(self.get_following_user())

    #팔로워 수 반환
    def get_num_of_follower(self):
        return len(self.get_follower_user())

    #유저가 생성한 플레이리스트 수 반환
    def get_num_of_playlists(self):
        return len(self.get_playlists())

    #팔로잉 유저 객체의 리스트 반환
    def get_following_user(self):
        return [i for i in self.follow.all()]
    
    #팔로우 유저 객체의 리스트 반환
    def get_follower_user(self):
        return [i for i in Profile.objects.filter(follow=self.user)]
    
    #유저가 생성한 플레이리스트객체의 리스트 반환
    def get_playlists(self):
        return [i for i in Playlist.objects.filter(writer=self.user)]
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class MusicServiceAccount(models.Model):
    class MusicService(models.IntegerChoices):
        MELON = 1
        GENIE = 2
        FLO = 3
        VIBE = 4
        BUGS = 5

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ownerMusicAccount')
    music_provider = models.IntegerField(choices=MusicService.choices)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_music_provider_display()} {self.username}"


