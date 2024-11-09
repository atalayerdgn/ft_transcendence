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
import requests
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action

class AuthHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthServiceImpl(AuthRepositoryImpl())

    # Kullanıcı girişi
    def login(self, request):
        serializer = LoginSerializer(data=request.data)  # Kullanıcı verilerini doğrulamak için LoginSerializer kullanılır
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        result = self.service.login(serializer.validated_data)  # Doğrulanan verilerle login servisi çağrılır

        # Login başarılıysa geçici bir token ile kullanıcıya 2FA doğrulama isteği gönderilir
        if result['success']:
            return Response({
                'message': '2FA code sent to your email, please validate',
                'temp_token': result['temp_token']
            }, status=status.HTTP_200_OK)
            
        # Login başarısızsa hata mesajı döner
        return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

    # 2FA doğrulama    
    def validate_twofa(self, request):
        serializer = TwoFASerializer(data=request.data)  # 2FA kodu doğrulamak için TwoFASerializer kullanılır
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        twofa_code = serializer.validated_data.get('twofa_code')

        # JWT token'ı Header'dan al
        auth_header = request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Bearer '):
            return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]  # 'Bearer ' kısmını ayırarak token al

        # Token'ı çözümle ve kullanıcıyı al
        user = self.service.get_user_from_token(token)
        if user is None:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        # 2FA kodunu kontrol et
        validation_result = self.service.validate_twofa(user, twofa_code)
        if validation_result:
            return Response({'message': '2FA validation successful'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid 2FA code'}, status=status.HTTP_400_BAD_REQUEST)
    
     # 42 OAuth giriş yönlendirmesi
    
    @csrf_exempt
    def login_with_42(self, request):
        logger.error("Login with 42")
        logger.debug("Login with 42")
        client_id = "u-s4t2ud-f0a16fd8008b548e10e481a206cb0700607774c18bb30aca8d7208d9f1a93bf5"
        redirect_uri = "http://localhost:8004/users/oauth_callback/"
        authorize_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=public&prompt=consent"
        return redirect(authorize_url)
    
    # OAuth callback işlemi
    @csrf_exempt
    def oauth_callback(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'Authorization code is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Token almak için 42 API'ye istek gönderin
        client_id = "u-s4t2ud-f0a16fd8008b548e10e481a206cb0700607774c18bb30aca8d7208d9f1a93bf5"
        client_secret = "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"
        redirect_uri = "https://www.google.com"
        
        # Token almak için POST isteği oluşturun
        token_response = requests.post(
            "https://api.intra.42.fr/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
        )
        
        if token_response.status_code != 200:
            return Response({'error': 'Failed to obtain access token'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response.json().get('access_token')
        
        # 42 API'den kullanıcı bilgilerini almak için token kullanın
        user_info_response = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_info_response.status_code != 200:
            return Response({'error': 'Failed to fetch user information'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_response.json()
        
        # Kullanıcıyı veritabanına kaydetme veya güncelleme işlemi
        user, created = User.objects.get_or_create(
            username=user_info.get('login'),
            defaults={
                "first_name": user_info.get('first_name'),
                "last_name": user_info.get('last_name'),
                "email": user_info.get('email')
            }
        )

        if not created:
            user.first_name = user_info.get('first_name')
            user.last_name = user_info.get('last_name')
            user.email = user_info.get('email')
            user.save()

        # JWT token ile kullanıcıya döndürme
        jwt_token = Utils.generate_token(user)
        return Response({'token': jwt_token, 'message': 'User logged in successfully'}, status=status.HTTP_200_OK)


class UserManagementHandler(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserServiceImpl(UserRepositoryImpl())
        
    #get_user_by_id
    def get_user_by_id(self, request):
        user_id = request.query_params.get('id')  # Kullanıcı ID'si query parametrelerinden alınır
        if not user_id:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if not uuid.UUID(user_id):  # ID'nin UUID formatında olup olmadığını kontrol eder
                return Response({'error': 'Invalid user ID format. Please provide a valid UUID.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid user ID format. Please provide a valid UUID.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user, message = self.service.get_user_by_id(UUID(user_id))  # Kullanıcıyı ID ile alır
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)  # Kullanıcı bulunamazsa hata mesajı döner
    
    
    #get_user_by_username
    def get_user_by_username(self, request):
        # Authorization başlığından token alınır
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1] # Bearer token alınır
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Token'dan kullanıcı adı çözülür
            decoded = Utils.decode_token(token)
            username = decoded.get('username') # Kullanıcı adı alınır
            
            if not username:
                return Response({'error': 'Username not found in token'}, status=status.HTTP_400_BAD_REQUEST)

            # Kullanıcı adı ile veritabanından kullanıcı bulunur
            user, message = self.service.get_user_by_username(username)
            if user:
                serializer = UserSerializer(user) # Kullanıcı verileri serialize edilir
                return Response(serializer.data, status=status.HTTP_200_OK)
        
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        except jwt.ExpiredSignatureError: # Token süresi dolmuşsa hata döner
            return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED),
        
        except jwt.InvalidTokenError: # Geçersiz token hatası döner
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except ValueError as e: # Diğer hatalar için hata döner
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED),
        

    #get_user_by_email
    def get_user_by_email(self, request):
        email = request.query_params.get('email') # E-posta adresi query parametrelerinden alınır
        if not email: # E-posta adresi girilmediyse hata döner
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, message = self.service.get_user_by_email(email) # E-posta adresine göre kullanıcı alınır
        if user: # Kullanıcı bulunduysa veriler serialize edilir
            serializer = UserSerializer(user) # Kullanıcı verileri serialize edilir yani düzenlenir
            return Response(serializer.data, status=status.HTTP_200_OK) # Kullanıcı verileri döner
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND) # Kullanıcı bulunamazsa hata mesajı döner

    #create_user
    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data) # Kullanıcı verilerini doğrulamak için CreateUserSerializer kullanılır
        if not serializer.is_valid(): # Eğer veriler doğrulanamazsa hata döner
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        success, message = self.service.create_user(serializer.validated_data) # Doğrulanan verilerle kullanıcı oluşturma servisi çağrılır
        if success:
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    #delete_user
    def delete_user(self, request):
        user_id = request.query_params.get('id') # Kullanıcı ID'si query parametrelerinden alınır
        if not user_id: # Eğer ID girilmediyse hata döner
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

        success, message = self.service.delete_user(UUID(user_id)) # Kullanıcı ID'si ile kullanıcı silme servisi çağrılır
        if success:
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    
    #list_users
    def list_users(self, request): 
        user_list, message = self.service.get_all_users() # Tüm kullanıcıları alır
        if user_list:
            serializer = UserSerializer(user_list, many=True) # Kullanıcı verileri serialize edilir
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    #update_user
    def update_user(self, request):
        # Authorization başlığından token alınır
        token = request.META.get('HTTP_AUTHORIZATION') 
        if not token or not token.startswith('Bearer '):
            return Response({'error': 'Authorization token is missing or invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        # İstek verilerini al ve servise gönder
        result, message, new_token = self.service.update_user(token, request.data)
        if result:
            return Response({
                'message': 'User updated successfully',
                'token': new_token,
                'username' : request.data.get('username'),
                'email' : request.data.get('email'),
                'first_name' : request.data.get('first_name'),
                'last_name' : request.data.get('last_name','lastname yok amk'),
            }, status=status.HTTP_200_OK)

        # Başarısız durum
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    @csrf_exempt    
    def upload_avatar(self, request):
        user_id = request.query_params.get('id')  # Kullanıcı ID'sini alın
        if not user_id:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, _ = self.service.get_user_by_id(UUID(user_id))
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Avatar dosyasını al
        avatar_file = request.FILES.get('profile_picture')
        if not avatar_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Servis katmanında güncelleme işlemini yap
        success, message = self.service.update_avatar(UUID(user_id), avatar_file)
        if success:
            return Response({'message': message, 'avatar': avatar_file.name}, status=status.HTTP_200_OK)
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
