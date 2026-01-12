# friends/serializers.py
from rest_framework import serializers
from accounts.models import Utilisateur
from .models import DemandeAmi

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email']

class DemandeAmiSerializer(serializers.ModelSerializer):
    expediteur = UtilisateurSerializer(read_only=True)
    destinataire = UtilisateurSerializer(read_only=True)

    class Meta:
        model = DemandeAmi
        fields = ['id', 'expediteur', 'destinataire', 'accepte', 'date_demande']
