from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField( upload_to='profile-image')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='user_followers')


    def __str__(self):
        return self.username
