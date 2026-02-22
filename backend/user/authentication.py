from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

User = get_user_model()


class TelegramBotAuthentication(authentication.BaseAuthentication):
    HEADER_BOT_TOKEN = "HTTP_X_TELEGRAM_BOT_API_TOKEN"
    HEADER_USER_ID = "HTTP_X_TELEGRAM_USER_ID"

    def authenticate(self, request):
        bot_token = request.META.get(self.HEADER_BOT_TOKEN)
        tg_user_id = request.META.get(self.HEADER_USER_ID)

        if not bot_token or not tg_user_id:
            return None

        expected = getattr(settings, "TELEGRAM_BOT_API_TOKEN", None)
        if not expected or bot_token != expected:
            raise exceptions.AuthenticationFailed("Invalid telegram bot token")

        try:
            tg_user_id_int = int(tg_user_id)
        except (TypeError, ValueError):
            raise exceptions.AuthenticationFailed("Invalid telegram user id")

        user = self._get_or_create_telegram_user(tg_user_id_int)

        return (user, None)

    def authenticate_header(self, request):
        return "TelegramBot"

    def _get_or_create_telegram_user(self, tg_user_id: int):
        user, created = User.objects.get_or_create(
            telegram_user_id=tg_user_id,
            defaults={
                "username": f"tg_{tg_user_id}"
            },
        )
        if created:
            user.set_unusable_password()

            if hasattr(user, "auth_source"):
                user.auth_source = "telegram"
                user.save(update_fields=["password", "auth_source"])
            else:
                user.save(update_fields=["password"])

        return user
