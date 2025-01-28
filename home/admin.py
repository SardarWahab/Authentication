from django.contrib import admin
from .models import Blog, Comment

from .models import Blog
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')  # Remove `likes` and `dislikes`
    list_filter = ('created_at',)  # Optional: Add filters
    search_fields = ('title', 'content')  # Optional: Add search functionality
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'likes_count', 'dislikes_count')

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

    def dislikes_count(self, obj):
        return obj.dislikes.count()
    dislikes_count.short_description = 'Dislikes'

admin.site.register(Blog, BlogAdmin)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    search_fields = ('content', 'user__username', 'blog__title')
    list_filter = ('created_at', 'blog')
