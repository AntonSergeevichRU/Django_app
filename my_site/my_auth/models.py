from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

def user_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return 'users/user_{pk}/avatar/{filename}'.format(
        pk=instance.user.pk,
        filename=filename,
    )


class Profile(models.Model):

    class Meta:

        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Биография')
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, upload_to=user_avatar_directory_path, verbose_name='Изображение')




