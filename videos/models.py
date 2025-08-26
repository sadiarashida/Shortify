from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Comment(models.Model):
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    comment = models.CharField(max_length=250, default="unavailable")
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(null=True, upload_to="images")
    ratedUsers = models.ManyToManyField(User, related_name="ratedUsersComment")

    def __str__(self):
        return self.comment[:30]

    class Meta:
        ordering = ["-created"]


class VideoRating(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    RATING_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey("Video", on_delete=models.CASCADE)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "video")  # One rating per user per video

    def __str__(self):
        return f"{self.user.username} {self.rating}d {self.video.title}"


class Video(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    video = models.FileField(upload_to="videos")
    thumbnail = models.ImageField(upload_to="images")
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    views = models.IntegerField(default=0)
    comments = models.ManyToManyField(
        Comment,
        related_name="comments",
    )
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    ratedUsers = models.ManyToManyField(User, related_name="video_ratings")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    username = models.CharField(max_length=30, default="Anonymous")
    picture = models.ImageField(upload_to="images", blank=True, null=True)
    description = models.CharField(max_length=50, blank=True)
    videos = models.ManyToManyField(Video, related_name="user_videos")

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-username"]
