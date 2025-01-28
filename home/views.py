from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment # Assuming a BlogForm exists

@login_required
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')  # Fetch all blogs
    print(f"Blogs: {blogs}")  # Debugging output
    return render(request, 'home.html', {'blogs': blogs})

@login_required
def blog_detail(request, blog_id):
    pass
@login_required
def add_comment(request, blog_id):
   pass

@login_required
def upload_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Ensure image file is being uploaded

        if title and content:  # Validate required fields
            blog = Blog(
                title=title,
                content=content,
                image=image,
                created_at=now(),  # Automatically set the current timestamp
            )
            blog.save()
            messages.success(request, "Blog uploaded successfully!")
            return redirect('home')  # Redirect after successful upload
        else:
            messages.error(request, "Title and content are required fields.")
            return redirect('upload_blog')  # Redirect back to the form if validation fails

    # Render the form for GET requests
    return render(request, 'auth/upload_blog.html')
