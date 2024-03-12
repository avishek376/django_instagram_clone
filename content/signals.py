from django.db.models.signals import pre_save, post_save
from .models import PostMedia, PostComments, UserPost
from django.dispatch import receiver
from .tasks import process_media


# These receivers are called when the model object is updated or saved every time,
# so, if we don't want to call them every time we have to push some condition over them to restrict


# TODO:: Implement CELERY tasks for media processing

@receiver(post_save, sender=PostMedia)
def process_media(sender, instance, **kwargs):
    print("SIGNALS:: Inside Post Process Media Signal")
    # process_media.delay(instance)


@receiver(post_save, sender=UserPost)
def send_new_post_notification(sender, instance, **kwargs):
    if instance.is_published:
        print("SIGNALS:: send some notifications to user followers")
    else:
        print("SIGNALS:: not going to send some notifications")


@receiver(post_save, sender=PostComments)
def profanity_filter(sender, instance, **kwargs):
    print("SIGNALS:: Profanity filter called")


@receiver(pre_save, sender=PostComments)
def send_notification(sender, instance, **kwargs):
    print("SIGNALS:: Send notification to the post author")
