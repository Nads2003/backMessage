from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import MessageSerializer
from accounts.models import Utilisateur

class MessagesConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(status=404)

        messages = Message.objects.filter(
            conversation=conversation
        ).order_by("date_envoi")

        # 🔥 marquer comme lu (sauf mes messages)
        Message.objects.filter(
            conversation=conversation,
            est_lu=False
        ).exclude(expediteur=request.user).update(est_lu=True)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class ConversationPriveeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            autre_user = Utilisateur.objects.get(id=user_id)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=404)

        # chercher conversation existante
        conversation = (
            Conversation.objects
            .filter(participants=request.user)
            .filter(participants=autre_user)
            .first()
        )

        # sinon créer
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, autre_user)

        return Response({
            "id": conversation.id
        })
# chat/views.py
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, Message

class MessageVocalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation")
        vocal = request.FILES.get("vocal")

        conversation = Conversation.objects.get(id=conversation_id)

        msg = Message.objects.create(
            expediteur=request.user,
            conversation=conversation,
            vocal=vocal
        )

        return Response(MessageSerializer(msg).data)
