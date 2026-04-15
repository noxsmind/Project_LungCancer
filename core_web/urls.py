from django.contrib import admin
from django.urls import path
from prediksi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rute Autentikasi
    path('login/', views.halaman_login, name='login'),
    path('logout/', views.halaman_logout, name='logout'),
    path('register/', views.halaman_register, name='register'), # <--- BARIS BARU
    
    # Rute Utama
    path('', views.halaman_deteksi, name='deteksi'),
    path('profil/', views.halaman_profil, name='profil'),
]