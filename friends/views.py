from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from accounts.models import Utilisateur
from accounts.serializers import UtilisateurChatSerializer,UtilisateurProfileSerializer
from .models import DemandeAmi
from .serializers import UtilisateurSerializer, DemandeAmiSerializer

# 🔹 Liste des utilisateurs non-amis
# Liste des utilisateurs non-amis et sans demande en attente
class ListeNonAmisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # tous les utilisateurs sauf celui connecté
        tous_les_users = Utilisateur.objects.exclude(id=user.id)

        # IDs des utilisateurs déjà amis
        amis_ids = DemandeAmi.objects.filter(
            Q(expediteur=user) | Q(destinataire=user),
            accepte=True
        ).values_list('expediteur_id', 'destinataire_id')

        amis_ids = set([i for tup in amis_ids for i in tup if i != user.id])

        # IDs des utilisateurs à qui on a déjà envoyé une demande en attente
        demandes_envoyees_ids = DemandeAmi.objects.filter(
            expediteur=user,
            accepte=False
        ).values_list('destinataire_id', flat=True)

        # Exclure amis et utilisateurs avec demande en attente
        non_amis = tous_les_users.exclude(id__in=amis_ids.union(set(demandes_envoyees_ids)))

        serializer = UtilisateurSerializer(non_amis, many=True)
        return Response(serializer.data)

# 🔹 Liste des amis acceptés
class ListeAmisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        demandes = DemandeAmi.objects.filter(
            Q(expediteur=user) | Q(destinataire=user),
            accepte=True
        )
        amis = [d.destinataire if d.expediteur == user else d.expediteur for d in demandes]
        serializer = UtilisateurProfileSerializer(amis, many=True,context={"request": request})
        return Response(serializer.data)


# 🔹 Envoyer une demande
class EnvoyerDemandeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        destinataire_id = request.data.get("destinataire_id")
        if not destinataire_id:
            return Response({"error": "Destinataire requis"}, status=400)
        if int(destinataire_id) == user.id:
            return Response({"error": "Vous ne pouvez pas vous ajouter vous-même"}, status=400)
        if DemandeAmi.objects.filter(expediteur=user, destinataire_id=destinataire_id).exists():
            return Response({"error": "Demande déjà envoyée"}, status=400)

        demande = DemandeAmi.objects.create(expediteur=user, destinataire_id=destinataire_id)
        serializer = DemandeAmiSerializer(demande)
        return Response(serializer.data)


# 🔹 Annuler une demande envoyée
class AnnulerDemandeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        destinataire_id = request.data.get("destinataire_id")
        try:
            demande = DemandeAmi.objects.get(expediteur=user, destinataire_id=destinataire_id, accepte=False)
            demande.delete()
            return Response({"message": "Demande annulée"})
        except DemandeAmi.DoesNotExist:
            return Response({"error": "Demande non trouvée"}, status=404)


# 🔹 Liste des demandes reçues
class ListeDemandesRecuesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        demandes = DemandeAmi.objects.filter(destinataire=user, accepte=False)
        serializer = DemandeAmiSerializer(demandes, many=True)
        return Response(serializer.data)


# 🔹 Liste des demandes envoyées
class ListeDemandesEnvoyeesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        demandes = DemandeAmi.objects.filter(expediteur=user, accepte=False)
        serializer = DemandeAmiSerializer(demandes, many=True)
        return Response(serializer.data)


# 🔹 Répondre à une demande reçue
class RepondreDemandeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        demande_id = request.data.get("demande_id")
        accepter = request.data.get("accepter", True)
        try:
            demande = DemandeAmi.objects.get(id=demande_id, destinataire=user, accepte=False)
            if accepter:
                demande.accepte = True
                demande.save()
            else:
                demande.delete()
            return Response({"message": "Réponse enregistrée"})
        except DemandeAmi.DoesNotExist:
            return Response({"error": "Demande non trouvée"}, status=404)
        

class ListeAmisChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 🔹 Récupérer toutes les demandes acceptées où l'utilisateur est impliqué
        demandes = DemandeAmi.objects.filter(
            (Q(expediteur=user) | Q(destinataire=user)),
            accepte=True
        )

        # 🔹 Extraire les amis
        amis = [
            d.destinataire if d.expediteur == user else d.expediteur
            for d in demandes
        ]

        # 🔹 Serializer avec context pour get_last_message
        serializer = UtilisateurChatSerializer(
            amis, many=True, context={'request': request}
        )

        return Response(serializer.data)
