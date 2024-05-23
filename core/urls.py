from django.urls import path

from . import views


urlpatterns = [
    path("rooms/<str:room_name>/messages", views.RoomMessageList.as_view(), name="room-messages-list"),
]
