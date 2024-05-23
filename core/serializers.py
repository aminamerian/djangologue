from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.TimeField()
    username = serializers.CharField(source="user.username")
    created_at = serializers.DateTimeField()
