from rest_framework import serializers
from .models import Conversation, Groupe, Message
from accounts.serializers import UtilisateurChatSerializer

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    expediteur = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "contenu",
            "vocal",
            "date_envoi",
            "est_lu",
            "expediteur"
        ]

    def get_expediteur(self, obj):
        return {
            "id": obj.expediteur.id,
            "username": obj.expediteur.username
        }

class ConversationSerializer(serializers.ModelSerializer):
    participants = UtilisateurChatSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'date_creation']

class GroupeSerializer(serializers.ModelSerializer):
    createur = UtilisateurChatSerializer(read_only=True)
    membres = UtilisateurChatSerializer(many=True, read_only=True)

    class Meta:
        model = Groupe
        fields = ['id', 'nom', 'createur', 'membres', 'date_creation']
