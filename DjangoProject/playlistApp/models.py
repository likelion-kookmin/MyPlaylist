from django.db import models
from django.conf import settings

# Create your models here.

#플레이 리스트 모델
class Playlist(models.Model):
    title = models.CharField(max_length= 200) #플레이리스트 제목
    explain = models.TextField() #플레이리스트 설명 (+해시태그)
    look = models.IntegerField(default= 0) #플레이리스트 조회수
    image = models.ImageField(blank = True, upload_to = 'playlistProfile/') #플레이리스트의 이미지
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='playlist_likes', blank = True) #플레이리스트 좋아요한 유저
    putIn = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='playlist_putIn', blank = True) #플레이리스트를 담은 유저
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name= 'playlist_wirter') #플레이리스트의 작성자

    #플레이리스트 제목 반환
    def __str__(self):
        return self.title

#각각 곡의 모델
class Song(models.Model):
    artist = models.CharField(max_length = 200) #곡의 아티스트
    title = models.CharField(max_length= 200) #곡의 제목
    album = models.CharField(max_length= 200) #곡의 앨범명
    time = models.DurationField() #곡의 재생시간
    albumArt = models.ImageField(upload_to= 'albumArt/') #곡의 앨범아트
    melonUid = models.IntegerField() #멜론에서의 곡 id
    genieUid = models.IntegerField() #지니에서의 곡 id
    bugsUid = models.IntegerField() #벅스에서의 곡 id
    floUid = models.CharField(max_length = 200) #flo에서의 곡 id - flo에서만 id가 string으로 저장됨.
    viveUid = models.IntegerField() #vive에서의 곡 id

    def __str__(self):
        return self.title

#플레이리스트와 노래를 연결해주는 모델
class Relationship(models.Model):
    index = models.IntegerField() #플레이리스트 내의 곡 순서
    playlistObj = models.ManyToManyField(Playlist, related_name = 'relate_to_playlist') #연결된 플레이리스트
    songObj = models.ManyToManyField(Song, related_name= 'relate_to_song') #연결된 곡