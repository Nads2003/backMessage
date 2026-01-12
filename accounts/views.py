from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UtilisateurChatSerializer
from .models import Utilisateur
from .serializers import UtilisateurSerializer


class InscriptionView(generics.CreateAPIView):
    """
    Vue pour l'inscription d'un utilisateur
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.AllowAny]
    
class ProfilView(APIView):
    """
    Vue pour récupérer les informations
    de l'utilisateur connecté
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        utilisateur = request.user

        return Response({
            "id": utilisateur.id,
            "nom_utilisateur": utilisateur.username,
            "email": utilisateur.email,
            "en_ligne": utilisateur.est_en_ligne,
            "derniere_activite": utilisateur.derniere_activite
        })
#liste des utilisateurs
