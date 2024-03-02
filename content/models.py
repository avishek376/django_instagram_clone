from django.db import models
from api.models import TimeStamp, UserProfile


# Create your models here.

class UserPost(TimeStamp):
    caption_text = models.CharField(max_length=50, null=True)
    # TODO:: location will be lat long for better implementation
    location = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post')
    is_published = models.BooleanField(default=False)


# def upload_validator(image):
#     pass


class PostMedia(TimeStamp):
    def media_name(instance, filename):
        ext = filename.split(".")[-1]
        # TODO:: Implement UUID instead of post_id
        return f"post_media/{instance.post.id}_{instance.sequence_index}.{ext}"

    media_file = models.ImageField(upload_to=media_name, )
    sequence_index = models.PositiveSmallIntegerField(default=0)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='media')

    class Meta:
        unique_together = ['post', 'sequence_index']


class PostLikes(TimeStamp):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        unique_together = ['post', 'liked_by']


class PostComments(TimeStamp):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=255)

