from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# For below abstract class tables won't be created when migrating
class TimeStamp(models.Model):
    """Timezone model which is applicable to all models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='profile')

    # TODO:: Add verification for size and type of image that is uploaded
    # TODO:: Modify the naming of the saved image...so that the update view becomes idempotent or compliant with REST
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
