from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = Utilisateur(
            username=validated_data['username'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
# accounts/serializers.py
from rest_framework import serializers
from chat.models import Conversation, Message
from accounts.models import Utilisateur

class UtilisateurChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = [
            "id",
            "username",
            "est_en_ligne",
            "last_message"
        ]

    def get_last_message(self, user):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None

        me = request.user

        # 🔹 Conversation entre moi et cet utilisateur (la plus récente)
        conversation = Conversation.objects.filter(
            participants=me
        ).filter(
            participants=user
        ).order_by('-date_creation').first()

        if not conversation:
            return None

        # 🔹 Dernier message dans cette conversation
        last_msg = Message.objects.filter(
            conversation=conversation
        ).order_by("-date_envoi").first()

        if not last_msg:
            return None

        return {
            "contenu": last_msg.contenu if last_msg.contenu else "🎤 Message vocal",
            "date_envoi": last_msg.date_envoi,
            "expediteur": last_msg.expediteur.username
        }
