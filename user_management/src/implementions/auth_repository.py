from typing import Tuple
from django.contrib.auth.hashers import check_password
from src.interface.auth_repository import AuthRepository
from src.models.models import User
from src.utils import Utils
from django.utils import timezone
import random
import datetime
import logging

# Logger'ı ayarla
logger = logging.getLogger(__name__)

class AuthRepositoryImpl(AuthRepository):
    #login methodu, kullanıcı adı ve şifre alır ve kullanıcıyı veritabanında arar
    def login(self, username: str, password: str) -> Tuple[str, bool]:
        try:
            logger.info(f"Trying to login with username: {username}")
            #Kullanıcıyı veritabanında ara
            saved_user = User.objects.get(username=username)
            if check_password(password, saved_user.password):
                #şiifre doğruysa token oluştur
                token = self.generate_token(saved_user)
                #2fa kodu oluştur
                twofa_code = self.set_twofa_code(saved_user)#eozdur
                #2fa kodunu kullanıcıya gönder
                success = self.send_2fa_code(saved_user.email, twofa_code)#eozdur
                if not success:
                    return "2FA code sent but failed", False  # Hata durumunu yanıtla
                return token, saved_user.email, True # token ve başarılı yanıtı döndür
            return "Wrong password", False
        except User.DoesNotExist:
            return "User not found", False
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")  # Hata logla
            return f"Error: {str(e)}", False

    def generate_token(self, user: User) -> str: #eozdur
        #Token oluştur
        payload = {#Token içeriği
            'username': user.username,#Kullanıcı adı
            'user_id': str(user.id),#user_id
        }#burada yapılan işlemler token içeriğini oluşturur
        return Utils.create_token(payload)

    def generate_2fa_code(self) -> str: #eozdur
        return str(random.randint(100000, 999999))

    def set_twofa_code(self, user: User) -> str: #eozdur
        code = self.generate_2fa_code()#random 2fa kodu oluştur
        user.twofa_code = code #2fa kodunu kullanıcıya ata
        user.twofa_code_expiry = timezone.now() + datetime.timedelta(minutes=5)  # 5 dakika geçerli
        user.save() #kullanıcıyı kaydet
        return code# 2fa kodunu döndür

    def send_2fa_code(self, email: str, code: str) -> bool: #eozdur
        logger.debug(f"Sending 2FA code {code} to {email}")
        subject = "Your 2FA Code"
        body = f"Your 2FA code is: {code}"
        #içeriği oluşturulan e-posta gönderilir
        success = Utils.send_email(email, subject, body)  # E-posta gönderme
        if success:
            logger.info("E-posta başarıyla gönderildi.")
        else:
            logger.error("E-posta gönderiminde bir hata oluştu.")
        return success

    def validate_twofa(self, email: str, twofa_code: str) -> Tuple[bool, str]: #eozdur
        try:
            #Kullanıcıyı veritabanında ara
            user = User.objects.get(email=email)
            #2fa kodunu kontrol et
            if user.twofa_code == twofa_code:
                #2fa kodu doğruysa
                user.save()#kullanıcıyı kaydet
                return True, "2FA code is valid."
            return False, "Invalid or expired 2FA code."
        except User.DoesNotExist:
            logger.error(f"Trying to validate 2FA code {twofa_code} for {email}")
            return False, "User not fouyyynd."
        except Exception as e:
            logger.error(f"Error during 2FA validation: {str(e)}")
            return False, f"Error: {str(e)}"