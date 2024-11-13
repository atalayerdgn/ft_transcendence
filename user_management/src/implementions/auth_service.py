from typing import Tuple
from src.implementions.auth_repository import AuthRepositoryImpl
from src.interface.auth_service import AuthService
from src.utils import Utils
from src.models.models import User
from django.utils import timezone
import logging

# Logger'ı ayarla
logger = logging.getLogger(__name__)


class AuthServiceImpl(AuthService):
    def __init__(self, auth_repository: AuthRepositoryImpl):
        self.auth_repository = auth_repository

    def login(self, validated_data: dict) -> dict:
        username = validated_data.get('username') # Kullanıcı adını al
        password = validated_data.get('password') # Şifreyi al
        
        # Kullanıcıyı login metodu ile al repository'den
        user = self.auth_repository.login(username, password)
        
        if user is None: # Kullanıcı yoksa hata döndür
            return {'success': False, 'error': "User not found or wrong password"}

        # 2FA ve token işlemleri burada yapılır
        try:
            # 2FA doğrulama işlemleri için geçici token oluştur
            temp_token = Utils.generate_token(user, is_2fa_validated=False)# Geçici token oluştur
            twofa_code = Utils.set_twofa_code(user)  # 2FA kodu oluştur
            success = Utils.send_2fa_code(user.email, twofa_code)  # 2FA kodunu gönder
            if not success: # Eğer 2FA kodu gönderilemediyse hata döndür
                return {'success': False, 'error': "2FA code sent but failed to deliver"}
            return { # İşlem başarılıysa geçici token'ı döndür
                'success': True, # İşlem başarılı
                'temp_token': temp_token # Geçici token'ı döndür
            }
        except Exception as e: # Hata olursa logla ve hata döndür
            logger.error(f"Error during login: {str(e)}")
            return {'success': False, 'error': f"Error: {str(e)}"}


    def validate_twofa(self, user: User, twofa_code: str) -> bool: # 2FA kodunu doğrula
        try:
            if user.twofa_code == twofa_code and user.twofa_code_expiry > timezone.now(): # 2FA kodu doğru ve süresi geçmemişse
                user.twofa_code = None # 2FA kodunu temizle neden ? -> önceki 2FA kodu ile tekrar doğrulama yapılmasın
                user.twofa_code_expiry = None # 2FA kodunun süresini temizle
                self.auth_repository.validate_twofa(user) # 2FA doğrulamasını yap
                logger.info(f"User {user.username} validated 2FA successfully.")
                return True
            return False
        except Exception as e:
            logger.error(f"Error during 2FA validation: {str(e)}")
            return False

    def get_user_from_token(self, token: str) -> User: # Token'dan kullanıcıyı al
        try:
            decoded_token = Utils.decode_token(token)  # Token'ı çöz
            user_id = decoded_token.get('user_id')  # Kullanıcı ID'sini al
            return self.auth_repository.get_user_by_id(user_id)  # Kullanıcıyı repository'den al
        except (ValueError, Exception) as e:
            logger.error(f"Error during token decoding: {str(e)}")
            return None
        
    #logout işlemi
    def logout(self, user: User) -> tuple:
        try:
            user.is_online = False  # Kullanıcıyı çevrimdışı yap
            user.save()  # Veritabanında güncelle
            
            logger.info(f"User {user.username} logged out successfully.")
            logger.info(f"User {user.username} is online: {user.is_online}")
            
            return True, "User logged out successfully."
        
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return False, "An error occurred during logout."
