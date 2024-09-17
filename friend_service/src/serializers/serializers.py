import uuid
from enum import unique

from rest_framework import serializers

from ..models.models import Friend, FriendRequest


class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend
        fields = [
            'user_id',
            'friend_list'
        ]


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_id = serializers.UUIDField()
    to_user_id = serializers.UUIDField()
    request_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = [
            'from_user_id',
            'to_user_id',
            'request_id',
        ]

class AcceptRequestSerializer(serializers.ModelSerializer):
    req_id = serializers.UUIDField()
    main_user = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)

    class Meta:
        fields = [
            'req_id',
            'main_user',
            'user_id'
        ]
