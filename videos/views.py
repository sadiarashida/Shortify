from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Comment, UserProfile, VideoRating
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth

# from moviepy.editor import *

# Create your views here.


@login_required
def upload_view(request):
    # Used When Query Search Used in Video Detail View to redirect to the search view.
    if request.GET.get("query"):
        return redirect("/videos/?query=" + request.GET.get("query"))
    if request.FILES.get("video"):
        if (
            request.POST.get("title")
            and request.FILES.get("thumbnail")
            and request.FILES.get("video")
            and request.POST.get("description")
        ):
            video = Video()
            video.title = request.POST.get("title")
            video.description = request.POST.get("description")
            video.thumbnail = request.FILES.get("thumbnail")
            video.video = request.FILES.get("video")
            video.user = request.user
            video.save()
            return redirect("/videos/" + str(video.id) + "/")

    return render(request, "videos/upload.html", {})


def videos_view(request):

    queryset_list = Video.objects.all()
    query = request.GET.get("query")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(user__username__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5)  # Show 25 comments per page
    page = request.GET.get("page")
    queryset = paginator.get_page(page)

    likes_percent = {}
    user_ratings = {}

    for i in range(0, len(queryset)):
        tempquery = queryset.object_list.all()[i]

        # Calculate like percentage
        if tempquery.dislikes == 0 and tempquery.likes == 0:
            likes_percent[tempquery.id] = 0
        elif tempquery.dislikes == 0 and tempquery.likes != 0:
            likes_percent[tempquery.id] = 100
        else:
            likes_percent[tempquery.id] = 100 * (
                tempquery.likes / (tempquery.likes + tempquery.dislikes)
            )

        # Check if current user has rated this video and how
        if request.user.is_authenticated:
            try:
                user_rating = VideoRating.objects.get(
                    user=request.user, video=tempquery
                )
                user_ratings[tempquery.id] = user_rating.rating  # 'like' or 'dislike'
            except VideoRating.DoesNotExist:
                user_ratings[tempquery.id] = None  # No rating yet
        else:
            user_ratings[tempquery.id] = None

    return render(
        request,
        "videos/videos.html",
        {
            "queryset": queryset,
            "likes_percent": likes_percent,
            "user_ratings": user_ratings,
        },
    )


@login_required
def like_comment(request, comment_id, video_id):

    comment = get_object_or_404(Comment, pk=comment_id)

    hasRated = False
    for rateduser in comment.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        comment.likes = comment.likes + 1
        comment.ratedUsers.add(request.user)
        comment.save()

    return redirect("/videos/" + str(video_id) + "/")


@login_required
def dislike_comment(request, comment_id, video_id):

    comment = get_object_or_404(Comment, pk=comment_id)

    hasRated = False
    for rateduser in comment.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        comment.dislikes = comment.dislikes + 1
        comment.ratedUsers.add(request.user)
        comment.save()

    return redirect("/videos/" + str(video_id) + "/")


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    hasRated = False
    for rateduser in video.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        video.likes = video.likes + 1
        video.ratedUsers.add(request.user)
        video.save()

    return redirect("/videos/" + str(video_id) + "/")


@login_required
def dislike_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    hasRated = False
    for rateduser in video.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        video.dislikes = video.dislikes + 1
        video.ratedUsers.add(request.user)
        video.save()

    return redirect("/videos/" + str(video_id) + "/")


@login_required
def like_video_from_list(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    # Get or create user rating for this video
    try:
        rating = VideoRating.objects.get(user=request.user, video=video)
        # User already has a rating for this video
        if rating.rating == VideoRating.LIKE:
            # User already liked, so remove the like (toggle off)
            rating.delete()
            video.likes = max(0, video.likes - 1)  # Prevent negative likes
        else:
            # User had disliked, now change to like
            rating.rating = VideoRating.LIKE
            rating.save()
            video.likes += 1
            video.dislikes = max(0, video.dislikes - 1)  # Remove previous dislike
    except VideoRating.DoesNotExist:
        # User hasn't rated this video yet, create new like
        VideoRating.objects.create(
            user=request.user, video=video, rating=VideoRating.LIKE
        )
        video.likes += 1

    video.save()

    # Get the current page number to redirect back to the same page
    page = request.GET.get("page", "1")
    query = request.GET.get("query", "")

    if query:
        return redirect(f"/videos/?page={page}&query={query}")
    else:
        return redirect(f"/videos/?page={page}")


@login_required
def dislike_video_from_list(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    # Get or create user rating for this video
    try:
        rating = VideoRating.objects.get(user=request.user, video=video)
        # User already has a rating for this video
        if rating.rating == VideoRating.DISLIKE:
            # User already disliked, so remove the dislike (toggle off)
            rating.delete()
            video.dislikes = max(0, video.dislikes - 1)  # Prevent negative dislikes
        else:
            # User had liked, now change to dislike
            rating.rating = VideoRating.DISLIKE
            rating.save()
            video.dislikes += 1
            video.likes = max(0, video.likes - 1)  # Remove previous like
    except VideoRating.DoesNotExist:
        # User hasn't rated this video yet, create new dislike
        VideoRating.objects.create(
            user=request.user, video=video, rating=VideoRating.DISLIKE
        )
        video.dislikes += 1

    video.save()

    # Get the current page number to redirect back to the same page
    page = request.GET.get("page", "1")
    query = request.GET.get("query", "")

    if query:
        return redirect(f"/videos/?page={page}&query={query}")
    else:
        return redirect(f"/videos/?page={page}")


def video_detail_view(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    videoUserName = video.user.username
    try:
        userprofile = UserProfile.objects.get(username=videoUserName)
    except UserProfile.DoesNotExist:
        userprofile = None

    recentvideos = Video.objects.all()
    tempvideos = []
    count = 0
    # adding first 4 new videos, not including the playing one, to the recommendations
    for recentvideo in recentvideos:
        if recentvideo.id != video_id:
            tempvideos.append(recentvideo)
            count = count + 1
            if count >= 4:
                break

    recentvideos = tempvideos

    queryset_list = video.comments.all()
    paginator = Paginator(queryset_list, 3)  # Show 25 comments per page
    # paginator = Paginator(comment_list, 1) # Show 25 comments per page
    page = request.GET.get("page")
    queryset = paginator.get_page(page)

    # Used When Query Search Used in Video Detail View to redirect to the search view.
    if request.GET.get("query"):

        return redirect("/videos/?query=" + request.GET.get("query"))

    if (
        request.method == "POST"
        and "submitComment" in request.POST
        and request.POST.get("textareaComment")
        and request.user.is_authenticated
    ):

        comment = Comment()
        comment.comment = request.POST.get("textareaComment")
        comment.user = request.user
        commentUserName = request.user.username
        try:
            commentUserProfile = UserProfile.objects.get(username=commentUserName)
            comment.picture = commentUserProfile.picture
        except UserProfile.DoesNotExist:
            # Don't set picture if UserProfile doesn't exist
            pass
        comment.save()
        video.comments.add(comment)

    videoUserName = video.user.username
    try:
        userprofile = UserProfile.objects.get(username=videoUserName)
    except UserProfile.DoesNotExist:
        userprofile = None
    # adding a view with every video detail GET request
    video.views = video.views + 1
    video.save()

    return render(
        request,
        "videos/videodetail.html",
        {
            "video": video,
            "queryset": queryset,
            "recentvideos": recentvideos,
            "userprofile": userprofile,
        },
    )
