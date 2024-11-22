# HTTP isteklerini gerçekleştirmek için kullanılan bir kütüphane.
import requests
# Django REST Framework'te HTTP yanıtları oluşturmak için kullanılır.
from rest_framework.response import Response
# HTTP durum kodlarını temsil eden modül.
from rest_framework import status
# Loglama işlemleri için logging modülü.
import logging
# Python'da tip tanımları için kullanılan modül.
from typing import Dict
# Servis ve repository arayüzleri.
from ..interface.gateway_service import GatewayService
from ..interface.gateway_repository import GatewayRepository

# Loglama için bir logger nesnesi tanımlanıyor.
logger = logging.getLogger('apigateway')

# Gateway iş mantığını yöneten sınıf.
class GatewayServiceImpl(GatewayService):
    def __init__(self, repository: GatewayRepository):
        # Repository, veri erişim işlemleri için kullanılır.
        self.repository = repository

    # HTTP isteklerini işleyen ana metot.
    def process_request(self, request: any, path: str) -> Response:
        # İlgili servis URL'sini almak için repository katmanını çağırır.
        base_url, error = self.repository.get_service_url(path)
        if error:
            # URL bulunamazsa 404 yanıtı döner.
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        # Tam URL'yi oluşturur.
        full_url = f"{base_url}/{path}"
        logger.info(f"Forwarding request to: {full_url}")

        # İsteğin parametrelerini alır.
        params = self._get_request_params(request)
        # HTTP isteğini repository'ye iletir.
        response, error = self.repository.forward_request(
            method=request.method.lower(),
            url=full_url,
            headers=dict(request.headers),
            params=params
        )

        if error:
            # İstek başarısız olursa 500 yanıtı döner.
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Dış servisten gelen yanıtı işleyip döner.
        return self._handle_response(response)

    # HTTP isteğinden parametreleri alır.
    def _get_request_params(self, request: any) -> Dict:
        params = {}
        # POST, PUT veya PATCH gibi gövdeli isteklerde gövdeyi ekler.
        if request.method.lower() in ['post', 'put', 'patch']:
            params['json'] = request.data if request.data else request.query_params.dict()
        else:
            # Diğer isteklerde sorgu parametrelerini ekler.
            params['params'] = request.query_params.dict()
        return params

    # Dış servisten gelen yanıtı işler.
    def _handle_response(self, response: requests.Response) -> Response:
        # Yanıt JSON ise JSON olarak döner.
        if response.headers.get('content-type') == 'application/json':
            return Response(response.json(), status=response.status_code)
        # Yanıt farklı türde ise ham veriyi döner.
        return Response(response.content, status=response.status_code)
