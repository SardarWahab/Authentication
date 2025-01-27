from django.contrib import admin
from .models import Blog, Comment

from .models import Blog
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'likes', 'dislikes')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    search_fields = ('content', 'user__username', 'blog__title')
    list_filter = ('created_at', 'blog')
