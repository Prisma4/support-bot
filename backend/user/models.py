from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models


class AuthSource(models.TextChoices):
    DJANGO = "django", "Django"
    TELEGRAM = "telegram", "Telegram"


class User(AbstractUser, PermissionsMixin):
    telegram_user_id = models.BigIntegerField(unique=True, null=True, blank=True)

    auth_source = models.CharField(
        max_length=16,
        choices=AuthSource.choices,
        default=AuthSource.DJANGO,
    )
