from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)  # Tracks users who liked
    dislikes = models.ManyToManyField(User, related_name='disliked_blogs', blank=True)  # Tracks users who disliked
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title} at {self.created_at}"
