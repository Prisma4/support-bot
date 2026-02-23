from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import AuthSource

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_tg_auth = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "telegram_user_id",
            "auth_source",
            "is_tg_auth"
        )
        read_only_fields = (
            "id",
        )

    def get_is_tg_auth(self, obj):
        return obj.auth_source == AuthSource.TELEGRAM
