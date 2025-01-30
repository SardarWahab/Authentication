from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment # Assuming a BlogForm exists
from django.views.decorators.cache import cache_page

@login_required
@cache_page(60 * 15)  # Cache the page for 15 minutes
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')  # Fetch all blogs
    print(f"Blogs in blog_list view: {blogs}")  # Debugging output
    return render(request, 'Blogs/home.html', {'blogs': blogs})

@login_required
@cache_page(60 * 15)  # Cache for 15 minutes
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if 'like' in request.POST:
            if request.user in blog.likes.all():
                blog.likes.remove(request.user)  # Remove the like if already liked
                messages.success(request, "You unliked this blog!")
            else:
                blog.likes.add(request.user)  # Add a like
                blog.dislikes.remove(request.user)  # Remove dislike if exists
                messages.success(request, "You liked this blog!")
            return redirect('blog_detail', blog_id=blog.id)

        # Handle dislike button
        elif 'dislike' in request.POST:
            if request.user in blog.dislikes.all():
                blog.dislikes.remove(request.user)  # Remove the dislike if already disliked
                messages.success(request, "You removed your dislike!")
            else:
                blog.dislikes.add(request.user)  # Add a dislike
                blog.likes.remove(request.user)  # Remove like if exists
                messages.success(request, "You disliked this blog!")
            return redirect('blog_detail', blog_id=blog.id)

        # Handle comment submission
        elif 'comment' in request.POST:
            content = request.POST.get('comment_content')
            if content:
                Comment.objects.create(blog=blog, user=request.user, content=content, created_at=now())
                messages.success(request, "Your comment has been posted!")
            else:
                messages.error(request, "Comment content cannot be empty.")
            return redirect('blog_detail', blog_id=blog.id)

    return render(request, 'Blogs/blog_detail.html', {'blog': blog, 'comments': comments})  

@login_required
def add_comment(request, blog_id):
   pass

@login_required
@cache_page(60 * 15)  # Cache for 15 minutes
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
                author=request.user  # Assign the logged-in user as the author
            )
            blog.save()
            messages.success(request, "Blog uploaded successfully!")
            return redirect('blog_list')  # Redirect after successful upload
        else:
            messages.error(request, "Title and content are required fields.")
            return redirect('upload_blog')  # Redirect back to the form if validation fails

    # Render the form for GET requests
    return render(request, 'Blogs/upload_blog.html')


@login_required
@cache_page(60 * 15)  # Cache for 15 minutes
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the logged-in user is the author of the blog
    if blog.author != request.user:
        messages.error(request, "You are not authorized to delete this blog.")
        return redirect('blog_detail', blog_id=blog_id)

    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully!")
        return redirect('blog_list')

    messages.error(request, "Invalid request.")
    return redirect('blog_detail', blog_id=blog_id)
