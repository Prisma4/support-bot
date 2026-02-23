from django.db import models

from user.models import User


class TicketStatus(models.IntegerChoices):
    CREATED = 1
    IN_PROGRESS = 2
    CLOSED = 3


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    processed_by = models.ManyToManyField(User, related_name='processed_tickets')

    name = models.CharField(max_length=100)

    status = models.IntegerField(choices=TicketStatus.choices, default=TicketStatus.CREATED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.name}"


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.text[:10]}"
