import uuid
from uuid import UUID
from venv import logger
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from src.models.models import User
import jwt
from django.conf import settings
import datetime
from src.utils import Utils
from src.implementions.auth_repository import AuthRepositoryImpl
from src.implementions.auth_service import AuthServiceImpl
from src.implementions.user_repository import UserRepositoryImpl
from src.implementions.user_service import UserServiceImpl
from src.serializers.serializers import UserSerializer, CreateUserSerializer, \
    LoginSerializer, TwoFASerializer , UpdateUserSerializer


class AuthHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthServiceImpl(AuthRepositoryImpl())

    def login(self, request): #eozdur değişiklik yapıldı
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        result = self.service.login(serializer.validated_data)
        
        if result['success']:
            return Response({
                'message': '2FA code sent to your email, please validate',
                'temp_token': result['temp_token']
            }, status=status.HTTP_200_OK)
            
        return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
    
    def validate_twofa(self, request): #eozdur
        serializer = TwoFASerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        twofa_code = serializer.validated_data.get('twofa_code')

        # JWT token'ı al
        auth_header = request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Bearer '):
            return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]  # 'Bearer ' kısmını ayır

        # Token'ı çözümle ve kullanıcıyı al
        user = self.get_user_from_token(token)
        if user is None:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        # 2FA kodunu kontrol et
        validation_result = self.service.validate_twofa(user, twofa_code)
        if validation_result:
            return Response({'message': '2FA validation successful'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid 2FA code'}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_from_token(self, token): #eozdur
        try:
            decoded_token = Utils.decode_token(token)  # Burada decode_token metodunu kullanıyoruz
            user_id = decoded_token.get('user_id')  # Burada user_id alanını kullanıyoruz
            return User.objects.get(id=user_id)  # Kullanıcıyı veritabanından al
        except (ValueError, User.DoesNotExist):
            return None
            

class UserManagementHandler(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserServiceImpl(UserRepositoryImpl())

    def get_user_by_id(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if not uuid.UUID(user_id):
                return Response({'error': 'Invalid user ID format. Please provide a valid UUID.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid user ID format. Please provide a valid UUID.'},
                            status=status.HTTP_400_BAD_REQUEST)
        user, message = self.service.get_user_by_id(UUID(user_id))
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    def get_user_by_username(self, request): #eozdur değişiklik yapıldı
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]  # Token'ı al
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Token'ı çözümle ve username'i al
            decoded = Utils.decode_token(token)  # Burada decode_token metodunu kullanıyoruz
            username = decoded.get('username')  # Token'dan username'i al
            
            if not username:
                return Response({'error': 'Username not found in token'}, status=status.HTTP_400_BAD_REQUEST)

            user, message = self.service.get_user_by_username(username)
            if user:
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    def get_user_by_email(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, message = self.service.get_user_by_email(email)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        success, message = self.service.create_user(serializer.validated_data)
        if success:
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    def delete_user(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

        success, message = self.service.delete_user(UUID(user_id))
        if success:
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    def list_users(self, request):
        user_list, message = self.service.get_all_users()
        if user_list:
            serializer = UserSerializer(user_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    from rest_framework import status

    def update_user(self, request): #eozdur
        # Authorization başlığından token'ı al
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token or not token.startswith('Bearer '):
            return Response({'error': 'Authorization token is missing or invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        token = token.split()[1]  # Bearer kısmını atla
        try:
            # Token'ı çözümle
            decoded_token = Utils.decode_token(token)
            current_user = decoded_token.get('username')  # Token'dan kullanıcı adını al
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Kullanıcı bilgilerini güncellemek için gelen verileri doğrula
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Eğer token'dan alınan kullanıcı ile güncellenmek istenen kullanıcı eşleşmiyorsa hata ver
        if current_user != serializer.validated_data['current_username']:
            return Response({'error': 'You do not have permission to update this user.'}, status=status.HTTP_403_FORBIDDEN)

        # Güncelleme işlemini gerçekleştirin
        success, message = self.service.update_user(serializer.validated_data)
        if success:
            # Yeni token için payload oluştur
            user = User.objects.get(username=serializer.validated_data['username'])
            payload = {
                'username': user.username,
                'user_id': str(user.id)
            }
            
            # Yeni token oluştur
            new_token = Utils.create_token(payload)
            
            return Response({
                'message': 'User updated successfully',
                'token': new_token,
                'username' : user.username,
                'email' : user.email,
                'first_name' : user.first_name,
                'last_name' : user.last_name           
            }, status=status.HTTP_200_OK)

        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    
