from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache  # Redis or local cache
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .models import User
import uuid


def register_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Basic validation
        if not email or not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        # ...existing code...
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

    return render(request, "auths/verify_email.html")


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
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, "auths/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")
