from django.contrib.auth.models import AbstractUser
from django.db import models
from annoying.fields import AutoOneToOneField

class User(AbstractUser):
    pass
    # followers = models.ManyToManyField("self", blank=True, related_name='followers')
    # following = models.ManyToManyField("self", blank=True, related_name='following')

#https://stackoverflow.com/questions/10602071/following-users-like-twitter-in-django-how-would-you-do-it
class UserProfile(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    follows = models.ManyToManyField('UserProfile', related_name='followed_by')


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.PROTECT, related_name="post_poster")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField()
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }