from rest_framework import serializers

from ticket.models import Ticket, TicketMessage, TicketStatus
from user.serializers import UserSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = (
            "user",
            "status",
            "processed_by"
        )


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "user",
            "name",
        )
        read_only_fields = (
            "user",
        )


class TicketMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = (
            "user",
            "ticket",
            "text",
        )
        read_only_fields = (
            "user",
        )

    def validate(self, attrs):
        if self.instance is None:
            ticket: Ticket = attrs.get("ticket")
            if ticket is None:
                return attrs

            if ticket.status == TicketStatus.CLOSED:
                raise serializers.ValidationError(
                    {"ticket": "This ticket is already closed."}
                )
        return attrs


class TicketMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TicketMessage
        fields = '__all__'
        read_only_fields = (
            "user",
        )
