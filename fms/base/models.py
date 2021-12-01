from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name='о себе')
    location = models.CharField(max_length=30, blank=True, verbose_name='город')
    avatar = models.ImageField(null=True, default="avatar.svg", verbose_name='фото профиля')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Topic(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, verbose_name='тема')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='пользователь')
    participants = models.ManyToManyField(User, related_name='participants', blank=True, verbose_name='участники')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = 'комната'
        verbose_name_plural = 'комнаты'

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return self.body[:50]


