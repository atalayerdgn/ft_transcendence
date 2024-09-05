from http import HTTPStatus
from uuid import UUID

from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from transandancefirst.usermanagment import serializers
from transandancefirst.usermanagment.models import UserManagement
from transandancefirst.usermanagment.repositoryimpl import UserRepositoryImpl
from transandancefirst.usermanagment.serializers import UserManagementSerializer
from transandancefirst.usermanagment.serviceimpl import UserServiceImpl

class UserManagementHandler(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserServiceImpl(UserRepositoryImpl())

    def get_user_by_id(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, message = self.service.get_user_by_id(int(user_id))
        if user:
            return Response(user, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    def get_user_by_username(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, message = self.service.get_user_by_username(username)
        return Response(user, status=status.HTTP_200_OK)

    def get_user_by_email(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, message = self.service.get_user_by_email(email)
        if user:
            return Response(user, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    def create_user(self, request):
        try:
            serializers = UserManagementSerializer(data=request.data)
            if serializers.is_valid():
                success, message = self.service.create_user(serializers.data)
            print(serializers.data)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete_user(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

        success, message = self.service.delete_user(UUID(user_id))
        if success:
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    def list_users(self, request):
        users = self.service.get_all_users()
        return Response(users, status=status.HTTP_200_OK)
