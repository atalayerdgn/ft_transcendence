# Django'nun admin paneli için gerekli modülü içe aktarır
from django.contrib import admin

# Django'nun URL yönlendirme işlevleri için gerekli modülleri içe aktarır
from django.urls import include, path


# URL yönlendirmelerini tanımlamak için bir liste oluşturur
urlpatterns = [
    # Yönetim paneline (admin) giden URL yolu
    # Kullanıcılar bu URL'yi ziyaret ederek Django yönetim paneline giriş yapabilirler
    path('admin/', admin.site.urls),

    # Dinamik olarak API Gateway'e giden URL yolu
    path('', include('routes.urls')),  # routes.urls'yi doğrudan köke bağlar
]
