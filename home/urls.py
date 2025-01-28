from django.urls import path
from . import views  # Import views from home app

urlpatterns = [
    path('', views.blog_list, name='blog_list'),  # Blog list view
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Blog detail view
    path('blog/<int:blog_id>/comment/', views.add_comment, name='add_comment'),  # Add comment view
    path('blog/upload/', views.upload_blog, name='upload_blog'),  # Blog upload view
    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    ]
