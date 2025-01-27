from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from home.views import blog_list, blog_detail, add_comment, upload_blog

urlpatterns = [
    path('', blog_list, name='blog_list'),  # Blog list view
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),  # Blog detail view
    path('blog/<int:blog_id>/comment/', add_comment, name='add_comment'),  # Add comment view
    path('blog/upload/', upload_blog, name='upload_blog'),  # Upload blog view
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

