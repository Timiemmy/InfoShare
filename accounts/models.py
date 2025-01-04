from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Contact(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = [
            '-created'
        ]

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'



class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField( upload_to='profile-image')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False)

    def __str__(self):
        return self.username


