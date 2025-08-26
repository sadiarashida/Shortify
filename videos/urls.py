from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.videos_view, name="videos"),
    path("upload/", views.upload_view, name="upload"),
    path("<int:video_id>/", views.video_detail_view, name="detail"),
    path(
        "like_comment/<int:comment_id>/<int:video_id>/",
        views.like_comment,
        name="like_comment",
    ),
    path(
        "dislike_comment/<int:comment_id>/<int:video_id>/",
        views.dislike_comment,
        name="dislike_comment",
    ),
    path("like_video/<int:video_id>/", views.like_video, name="like_video"),
    path("dislike_video/<int:video_id>/", views.dislike_video, name="dislike_video"),
    path(
        "like_video_from_list/<int:video_id>/",
        views.like_video_from_list,
        name="like_video_from_list",
    ),
    path(
        "dislike_video_from_list/<int:video_id>/",
        views.dislike_video_from_list,
        name="dislike_video_from_list",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
