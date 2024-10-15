import jwt
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import logging

# Logger'i ayarla
logger = logging.getLogger(__name__)

class Utils:
    @staticmethod
    #generate tokenda yapilan payload ile create_token fonksiyonu çağrilir
    #payload içeriği token içeriğini oluşturur
    def create_token(payload: dict) -> str:
        #expiration süresi 1 gün
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        #payload içeriğine expiration eklenir
        payload['exp'] = expiration
        #token oluşturulur
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    '''
    bunlar apigatewayde yapilacak!!!
    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
    '''

    @staticmethod
    def send_email(to_email, subject, body) -> bool: #eozdur
        from_email = settings.EMAIL_HOST_USER #e-posta adresi
        msg = MIMEMultipart() #e-posta içeriği
        msg['From'] = from_email #kimden
        msg['To'] = to_email #kime
        msg['Subject'] = subject #konu

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()  # Güvenliği etkinleştir
                server.login(from_email, settings.EMAIL_HOST_PASSWORD)  # Giriş yap
                server.send_message(msg)  # E-posta gönder
            logger.info(f"E-posta {to_email} adresine başariyla gönderildi.")
            return True
        except Exception as e:
            logger.error(f"E-posta gönderimi başarisiz: {str(e)}")  # Hata logla
            return False

'''
1. Kullanici Login İsteği Gönderir

    İstek: Kullanici, kullanici adi ve şifre bilgilerini girerek sisteme giriş yapmak ister.
    İşleyiş: Kullanici POST /login isteği gönderir.
        Kullanici adi ve şifre, LoginSerializer tarafindan doğrulanir.
        Eğer geçerli değilse (boş alanlar, hatali format vs.), 400 Hatali İstek (Bad Request) yaniti döner.
        
2. Giriş Doğrulama ve JWT Token Oluşturma

    İşleyiş: Giriş başarili olduğunda (şifre ve kullanici adi doğruysa), AuthRepositoryImpl sinifinda bu bilgileri kontrol ederiz:
        Doğruysa: Kullanici bulunduğunda, kullanici şifresi check_password fonksiyonu ile kontrol edilir.
        Eğer şifre doğruysa: Kullanici için bir JWT token oluşturulur. Bu token, kullaniciya ait kimlik bilgilerini (örneğin, username, user_id) içerir. 
        Token, Utils.create_token() fonksiyonu tarafindan oluşturulur:
            Token içerikleri: payload oluşturulur ve bu bilgiler token'a gömülür. Ek olarak, token'a bir expiration (sona erme) süresi eklenir, genellikle 1 gün (24 saat).
            Sonuç: Kullaniciya geçici olarak bir token ve 2FA kodu gönderilir.

3. İki Faktörlü Doğrulama (2FA) Kodu Oluşturma

    İşleyiş: Kullaniciya ek güvenlik sağlamak amaciyla bir 2FA kodu üretilir. Bu işlem set_twofa_code fonksiyonu ile gerçekleştirilir:
        2FA Kodu: Rastgele oluşturulan 6 haneli bir sayi, örneğin 347899.
        Geçerlilik süresi: Bu kod, 5 dakika boyunca geçerlidir. 5 dakikadan sonra kodun geçerliliği sona erer.
        Kodu veritabaninda kullaniciya kaydettikten sonra, 2FA kodu kullanicinin e-posta adresine gönderilir.

4. 2FA Kodunun Kullaniciya E-posta ile Gönderilmesi

    İşleyiş: E-posta gönderimi, Utils.send_email() fonksiyonu ile yapilir:
        E-posta başliği, konusu ve içeriği hazirlanir.
        SMTP protokolü kullanilarak e-posta gönderilir.
        Kullanici, e-posta adresine 2FA kodunu içeren bir mesaj alir (örneğin, “2FA Kodunuz: 347899”).

5. Kullanicinin 2FA Kodunu Girmesi

    İşleyiş: Kullanici giriş yaptiktan sonra e-posta adresine gönderilen 2FA kodunu girer ve bu kodu doğrulamak için yeni bir istek yapar:
        Kullanici bu kodu girdiğinde, POST /verify_2fa_code isteği gönderir.
        Kullanici kimliği ve girilen 2FA kodu ile veritabanindaki kod karşilaştirilir.

6. 2FA Kodunun Doğrulanmasi

    İşleyiş: Kullanicinin girdiği 2FA kodu veritabaninda saklanan kod ile karşilaştirilir. Eğer:
        Kod doğruysa ve geçerliyse: Kullaniciya kalici bir JWT token verilir, bu token ile sonraki tüm isteklerde kullanici kimliğini doğrular.
        Kod yanlişsa ya da süresi geçmişse: Kullaniciya 401 Yetkisiz (Unauthorized) hatasi döner, yani doğrulama başarisiz olur.

7. Token Kullanilarak Kimlik Doğrulama

    İşleyiş: Kullanici artik JWT token ile her yeni istekte kimliğini doğrulayabilir. Bu token:
        Her istekte istemciden (Authorization: Bearer <token>) header'inda gönderilir.
        Token geçerliliği apigateway tarafindan kontrol edilir.
        Eğer token süresi dolmuşsa ya da geçersizse, kullaniciya yeni bir token almak için tekrar giriş yapmasi istenir.  
        

'''