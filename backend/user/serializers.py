from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "telegram_user_id",
            "auth_source"
        )
        read_only_fields = (
            "id"
        )
