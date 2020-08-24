from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Each post should include the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later).

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.PROTECT, related_name="post_poster")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField()
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.email,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }
