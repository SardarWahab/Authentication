from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache  # Redis or local cache
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

def register_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        try:
            user = User.objects.create_user(email=email, username=username, password=password)
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return redirect("register")

        otp = uuid.uuid4().hex[:6].upper()
        cache.set(f"otp_{user.id}", otp, timeout=300)
        print(f"Generated OTP for {email}: {otp}")

        try:
            send_mail(
                "Email Verification",
                f"Your OTP is {otp}",
                "no-reply@example.com",
                [email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")
            return redirect("register")

        messages.success(request, "Account created successfully! Please verify your email.")
        return redirect("verify_email")
    
    cached_register_page = cache.get("register_page")
    if not cached_register_page:
        cached_register_page = render(request, "auth/register.html").content
        cache.set("register_page", cached_register_page, timeout=300)
    return cached_register_page


def verify_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email address.")
            return redirect("verify_email")

        cached_otp = cache.get(f"otp_{user.id}")

        if cached_otp and cached_otp == otp:
            user.is_active = True
            user.save()
            cache.delete(f"otp_{user.id}")
            messages.success(request, "Email verified successfully! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Invalid or expired OTP.")
            return redirect("verify_email")

    cached_verify_page = cache.get("verify_email_page")
    if not cached_verify_page:
        cached_verify_page = render(request, "auth/verify_email.html").content
        cache.set("verify_email_page", cached_verify_page, timeout=300)
    return cached_verify_page


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("blog_list")
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    cached_login_page = cache.get("login_page")
    if not cached_login_page:
        cached_login_page = render(request, "auth/login.html").content
        cache.set("login_page", cached_login_page, timeout=300)
    return cached_login_page


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


def home(request):
    cached_home_page = cache.get("home_page")
    if not cached_home_page:
        cached_home_page = render(request, "Blogs/home.html").content
        cache.set("home_page", cached_home_page, timeout=300)
    return cached_home_page
