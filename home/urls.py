from django.urls import path
from home.views import blog_list, blog_detail, add_comment

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/comment/', add_comment, name='add_comment'),
]
