from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ticket import views

router = DefaultRouter()

router.register('tickets', views.TicketsViewSet, basename='tickets')
router.register('ticket_messages', views.TicketMessagesViewSet, basename='ticket_messages')

staff_router = DefaultRouter()

router.register('tickets', views.StaffTicketsViewSet, basename='staff_tickets')
router.register('ticket_messages', views.StaffTicketMessagesViewSet, basename='staff_ticket_messages')

urlpatterns = [
    path('', include(router.urls), name='ticket'),
    path('', include(router.urls), name='ticket-staff'),
]
