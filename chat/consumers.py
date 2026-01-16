import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
import base64

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.user = self.scope["user"]

        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        if not await self.check_participant():
            await self.close()
            return

        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
     data = json.loads(text_data)

     message_text = data.get("message", "")
     local_id = data.get("localId")  # important pour le front
     vocal_base64 = data.get("vocal")  # si vocal envoyé en base64

    # Sauvegarder le message
     if message_text:
        msg = await self.save_message(message_text)
     elif vocal_base64:
        msg = await self.save_vocal_message(vocal_base64)
     else:
        return

    # ⚡ Vérifier si d'autres participants sont connectés sur cette conversation
     participants = await self.get_other_participants()
     if participants:
        # Si l'autre utilisateur est connecté, marquer comme lu
        msg.est_lu = True
        await database_sync_to_async(msg.save)()

    # BROADCAST À TOUS
     await self.channel_layer.group_send(
        self.room_group_name,
        {
            "type": "chat_message",
            "id": msg.id,
            "localId": local_id,
            "contenu": msg.contenu,
            "vocal": msg.vocal.url if msg.vocal else None,
            "est_lu": msg.est_lu,
            "expediteur": {
                "id": self.user.id,
                "username": self.user.username,
            }
        }
    )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "localId": event.get("localId"),
            "contenu": event["contenu"],
            "vocal": event.get("vocal"),
            "est_lu": event["est_lu"],
            "expediteur": event["expediteur"]
        }))

    @database_sync_to_async
    def save_message(self, contenu):
        from chat.models import Conversation, Message

        conversation = Conversation.objects.get(id=self.conversation_id)

        return Message.objects.create(
            expediteur=self.user,
            conversation=conversation,
            contenu=contenu,
            est_lu=False
        )

    @database_sync_to_async
    def save_vocal_message(self, vocal_base64):
        from chat.models import Conversation, Message
        import uuid

        conversation = Conversation.objects.get(id=self.conversation_id)
        format, audio_str = vocal_base64.split(';base64,')
        audio_data = ContentFile(base64.b64decode(audio_str), name=f"{uuid.uuid4()}.webm")

        return Message.objects.create(
            expediteur=self.user,
            conversation=conversation,
            vocal=audio_data,
            est_lu=False
        )

    @database_sync_to_async
    def check_participant(self):
        from chat.models import Conversation

        return Conversation.objects.filter(
            id=self.conversation_id,
            participants=self.user
        ).exists()
    @database_sync_to_async
    def get_other_participants(self):
     from chat.models import Conversation

     conversation = Conversation.objects.get(id=self.conversation_id)
    # Exclure l'expéditeur
     return conversation.participants.exclude(id=self.user.id).exists()
