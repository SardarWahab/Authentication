from django.urls import path
from home.views import blog_list, blog_detail, add_comment, upload_blog

urlpatterns = [
    path('', blog_list, name='blog_list'),  # Blog list view
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),  # Blog detail view
    path('blog/<int:blog_id>/comment/', add_comment, name='add_comment'),  # Add comment view
    path('blog/upload/', upload_blog, name='upload_blog'),  # Upload blog view
]

