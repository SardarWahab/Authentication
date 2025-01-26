from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment # Assuming a BlogForm exists

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = CommentForm()

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form
    })

@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', blog_id=blog.id)

    return HttpResponse("Invalid request")

from django.contrib import messages

@login_required
def upload_blog(request):
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
            return redirect('blog_list')  # Redirect to the blog list page
        else:
            messages.error(request, "Title and content are required fields.")
            return redirect('upload_blog')  # Redirect back to the form for correction

    return render(request, 'upload_blog.html')

