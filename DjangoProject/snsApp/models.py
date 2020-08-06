from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    # picture = models.ImageField(null=True, default=None)
    # music = models.ForeignKey()
    primaryMusicAccount = models.ForeignKey('MusicServiceAccount', on_delete=models.SET_NULL, default=None, null=True)
    follow = models.ManyToManyField(User, related_name='follow')

    def __str__(self):
        return f"{self.user.username} - {self.primaryMusicAccount}"
    
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
    music_service_code = models.IntegerField(choices=MusicService.choices)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_music_service_code_display()} {self.username}"


