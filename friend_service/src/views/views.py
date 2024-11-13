from venv import logger
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..implementions.friend_repository import FriendRepositoryImpl
from ..implementions.friend_service import FriendServiceImpl
from ..serializers.serializers import AcceptRequestSerializer, FriendSerializer, \
    FriendRequestSerializer


class FriendServiceHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = FriendServiceImpl(FriendRepositoryImpl())

    def send_request(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        from_user_id = serializer.validated_data.get('from_user_id')
        logger.error(f"from_user_id: {from_user_id}")
        to_user_id = serializer.validated_data.get('to_user_id')

        # Check if to_user_id exists
        #if not self.service.user_exists(to_user_id):
        #    return Response({"error": "to_user_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if self.service.user_exists(to_user_id) == False:
            return Response({"error": "to_user_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
         
        # Add to_user_id to from_user_id's friend list
        add_result, add_message = self.service.add_friend(from_user_id, to_user_id)
        if add_message:
            return Response(add_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Add from_user_id to to_user_id's friend list
        add_result, add_message = self.service.add_friend(to_user_id, from_user_id)
        if add_message:
            return Response(add_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"success": "Friend request sent and both users added to each other's friend list"}, status=status.HTTP_200_OK)

    def accept_request(self, request):
        serializers = AcceptRequestSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        success, message = self.service.accept_request(serializers.main_user, serializers.user_id, serializers.req_id)
        if message:
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(success, status=status.HTTP_200_OK)

    def reject_request(self, request):
        request_id = request.query_params.get('request_id')
        if not request_id:
            return Response("request_id is required",status=status.HTTP_400_BAD_REQUEST)
        success, message = self.service.reject_request(request_id)
        if message:
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(success, status=status.HTTP_200_OK)

    def get_friend_list(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response("user_id is required",status=status.HTTP_400_BAD_REQUEST)
        friends, message = self.service.get_friend_list(user_id)
        if message:
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        friend_list = list(friends)
        serializers = FriendSerializer(data=friend_list, many=True)
        if not serializers.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def get_friendship_requests(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # `self.service.get_friendship_requests(user_id)` metodu, FriendRequest nesnelerinden oluşan bir QuerySet döndürmelidir
        friendship_list, message = self.service.get_friendship_requests(user_id)

        if message:
            return Response({"error": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = FriendRequestSerializer(friendship_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)