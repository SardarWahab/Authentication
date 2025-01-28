from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    
    # Adding Many-to-Many fields for likes and dislikes
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_blogs', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title} at {self.created_at}"
