from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from videos.models import UserProfile
from django.conf import settings
from .forms import ProfileEditForm


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        user = auth.authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "accounts/login.html",
                {"error": "username or password is incorrect."},
            )
    else:
        return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    auth.logout(request)
    return redirect("home")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # User has info and wants an account now!
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.get(username=request.POST["username"])
                return render(
                    request,
                    "accounts/signup.html",
                    {"error": "Username has already been taken"},
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )

                # also create a UserProfile
                userprofile = UserProfile()
                userprofile.user = user
                userprofile.username = user.username
                if request.FILES.get("picture"):
                    userprofile.picture = request.FILES.get("picture")

                userprofile.save()

                auth.login(request, user)
                return redirect("home")
        else:
            return render(
                request, "accounts/signup.html", {"error": "Passwords must match"}
            )
    else:
        # User wants to enter info
        return render(request, "accounts/signup.html")


@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a profile if it doesn't exist
        user_profile = UserProfile.objects.create(
            user=request.user,
            username=request.user.username,
            description="",
        )

    return render(request, "accounts/profile.html", {"user_profile": user_profile})


@login_required
def profile_edit_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a profile if it doesn't exist
        user_profile = UserProfile.objects.create(
            user=request.user,
            username=request.user.username,
            description="",
        )

    if request.method == "POST":
        form = ProfileEditForm(
            request.POST, request.FILES, instance=user_profile, user=request.user
        )
        if form.is_valid():
            # Update user's first name and last name
            request.user.first_name = form.cleaned_data.get("first_name", "")
            request.user.last_name = form.cleaned_data.get("last_name", "")
            request.user.save()

            # Save the profile form
            form.save()

            return render(
                request,
                "accounts/profile_edit.html",
                {"form": form, "success": "Profile updated successfully!"},
            )
    else:
        form = ProfileEditForm(instance=user_profile, user=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})


def user_profile_view(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "accounts/user_not_found.html", {"username": username})

    try:
        user_profile = UserProfile.objects.get(user=profile_user)
    except UserProfile.DoesNotExist:
        # Create a profile if it doesn't exist
        user_profile = UserProfile.objects.create(
            user=profile_user,
            username=profile_user.username,
            description="",
        )

    # Get all videos uploaded by this user
    from videos.models import Video

    user_videos = Video.objects.filter(user=profile_user).order_by("-created")

    # Calculate likes percentage for each video
    likes_percent = {}
    for video in user_videos:
        total_ratings = video.likes + video.dislikes
        if total_ratings > 0:
            likes_percent[video.id] = (video.likes / total_ratings) * 100
        else:
            likes_percent[video.id] = 0

    context = {
        "profile_user": profile_user,
        "user_profile": user_profile,
        "user_videos": user_videos,
        "likes_percent": likes_percent,
        "total_videos": user_videos.count(),
        "total_views": sum(video.views for video in user_videos),
        "total_likes": sum(video.likes for video in user_videos),
    }

    return render(request, "accounts/user_profile.html", context)
