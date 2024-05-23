from rest_framework import permissions


class IsRoomMember(permissions.BasePermission):
    def has_permission(self, request, view):
        room_name = view.kwargs["room_name"]
        user = request.user
        return user.is_authenticated and user.memberships.filter(
            room__name=room_name, status="confirmed"
        ).exists()