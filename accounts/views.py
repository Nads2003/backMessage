from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Utilisateur
from .serializers import UtilisateurSerializer,UtilisateurProfileSerializer


class InscriptionView(generics.CreateAPIView):
    """
    Vue pour l'inscription d'un utilisateur
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.AllowAny]
    
class ProfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UtilisateurProfileSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)

from rest_framework.parsers import MultiPartParser, FormParser

class AvatarUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        avatar = request.FILES.get("avatar")

        if not avatar:
            return Response({"error": "Aucune image"}, status=400)

        user.avatar = avatar
        user.save()

        return Response({
            "message": "Photo mise à jour",
            "avatar": user.avatar.url
        })

