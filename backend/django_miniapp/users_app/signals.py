import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models import User, Profile


@receiver(post_delete, sender=User)
def post_delete_request(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.avatar.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Profile)
def replace_avatar_file(sender, instance, *args, **kwargs):
    """ Cleaning old file on uploading new one """

    if instance.pk:
        try:
            old_avatar = sender.objects.get(pk=instance.pk).avatar
            if old_avatar and instance.avatar != old_avatar:
                old_avatar_path = old_avatar.path
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)
        except sender.DoesNotExist:
            pass


@receiver(pre_save, sender=User)
def set_is_valid(sender, instance: User, *args, **kwargs):
    if instance.tg_id or instance.phone:
        instance.is_verified = True
    else:
        instance.is_verified = False
