# Loglama işlemleri için logging modülü.
import logging
# HTTP isteklerini gerçekleştirmek için kullanılan requests modülü.
import requests
# Tip tanımları için kullanılan modüller.
from typing import Dict, Tuple, Optional
# Gateway repository arayüzü.
from ..interface.gateway_repository import GatewayRepository
# Django ayarlarını almak için kullanılan modül.
from django.conf import settings

# Loglama için bir logger nesnesi tanımlanıyor.
logger = logging.getLogger('apigateway')

# Repository katmanı, veri erişim işlemlerini yöneten sınıftır.
class GatewayRepositoryImpl(GatewayRepository):
    # HTTP isteğini dış bir servise yönlendirir.
    def forward_request(self, method: str, url: str, headers: Dict, params: Dict) -> Tuple[Optional[requests.Response], str]:
        try:
            # İstek gönderilir.
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                **params
            )
            logger.info(f"Request successful: {url}")
            return response, ""
        except:
            # Başarısızlık durumunda loglama yapılır ve hata döner.
            logger.error(f"Request failed for URL: {url}")
            return None, "Request failed"

    # Servis URL'sini döner.
    def get_service_url(self, path: str) -> Tuple[Optional[str], str]:
        # Ayarlardaki rotalar üzerinden URL aranır.
        for route, url in settings.SERVICE_ROUTES.items():
            if path.startswith(route):
                return url, ""
        # Eşleşme bulunamazsa hata döner.
        logger.error(f"No matching service URL found for path: {path}")
        return None, "Service not found"
