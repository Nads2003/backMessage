from django.urls import path
from .views import InscriptionView, ProfilView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,   
)

urlpatterns = [
    path('auth/inscription/', InscriptionView.as_view(), name='inscription'),
    path('auth/connexion/', TokenObtainPairView.as_view(), name='connexion'),
    path('rafraichir/', TokenRefreshView.as_view(), name='rafraichir'),
    path('accounts/profile/', ProfilView.as_view(), name='profil'),
   
]
