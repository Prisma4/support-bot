from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ticket.models import Ticket, TicketMessage, TicketStatus
from ticket.serializers import TicketSerializer, TicketMessageSerializer, TicketCreateSerializer, \
    TicketMessageCreateSerializer


class TicketsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(user=user).select_related('user').prefetch_related('processed_by')

    def create(self, request):
        serializer = TicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj: Ticket = serializer.save(user=request.user)

        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=None, responses={204: None})
    @action(methods=['post'], detail=True)
    def close_ticket(self, request, pk: int):
        obj = get_object_or_404(self.get_queryset().exclude(status=TicketStatus.CLOSED), pk=pk)
        obj.status = TicketStatus.CLOSED
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TicketMessagesViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TicketMessageSerializer

    def get_queryset(self):
        user = self.request.user
        return TicketMessage.objects.filter(user=user).select_related('user')

    @action(methods=['post'], detail=True)
    def list_messages_for_ticket(self, request, pk: int):
        queryset = self.filter_queryset(self.get_queryset()).filter(ticket_id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TicketMessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj: TicketMessage = serializer.save(user=request.user)

        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)


class StaffTicketsViewSet(mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    permission_classes = [IsAdminUser, ]

    queryset = Ticket.objects.all().select_related('user').prefetch_related('processed_by')
    serializer_class = TicketSerializer

    @action(methods=['get'], detail=False)
    def get_pending_tickets(self, request):
        pending_tickets = self.get_queryset().filter(status=TicketStatus.CREATED)
        serializer = self.get_serializer(pending_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_active_tickets(self, request):
        active_tickets = self.get_queryset().filter(processed_by=request.user).exclude(status=TicketStatus.CLOSED)
        serializer = self.get_serializer(active_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffTicketMessagesViewSet(mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 mixins.ListModelMixin,
                                 GenericViewSet):
    permission_classes = [IsAdminUser, ]

    queryset = TicketMessage.objects.all().select_related('user')
    serializer_class = TicketMessageSerializer

    @action(methods=['post'], detail=True)
    def list_messages_for_ticket(self, request, pk: int):
        queryset = self.filter_queryset(self.get_queryset()).filter(ticket_id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TicketMessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj: TicketMessage = serializer.save(user=request.user)

        ticket: Ticket = obj.ticket
        ticket.status = TicketStatus.IN_PROGRESS
        ticket.processed_by.add(request.user)
        ticket.save()

        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)
