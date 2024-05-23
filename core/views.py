from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsRoomMember


class RoomMessageList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsRoomMember]

    def get_queryset(self):
        room_name = self.kwargs["room_name"]
        return Message.objects.filter(room__name=room_name).select_related(
            "room", "user"
        )
