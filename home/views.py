from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment # Assuming a BlogForm exists

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'auth/home.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    pass
@login_required
def add_comment(request, blog_id):
   pass

@login_required
def upload_blog(request):
    # if request.method == 'POST':
    #     title = request.POST['title']
    #     content = request.POST['content']
    #     image = request.FILES.get('image')  # Get the image file if uploaded

    #     # Create the new blog post
    #     blog = Blog(
    #         title=title,
    #         content=content,
    #         image=image,
    #         created_at=now(),  # <-- Use now() to set the current timestamp
    #     )
    #     blog.save()
        
    #     return redirect('blog_list')  # Redirect to the blog list after successful upload
    # else:
    #     return render(request, 'upload_blog.html') 
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if title and content:  # Ensure required fields are filled
            blog = Blog(
                title=title,
                content=content,
                image=image,
                created_at=now(),  # Automatically set the current timestamp
            )
            blog.save()
            messages.success(request, "Blog uploaded successfully!")
            return redirect('home')  # Redirect to the blog list page
        else:
            messages.error(request, "Title and content are required fields.")
            return redirect('upload_blog')  # Redirect back to the form for correction

    return render(request, 'auth/upload_blog.html')

