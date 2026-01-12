from django.db import models
from accounts.models import Utilisateur

# Conversation privée
class Conversation(models.Model):
    participants = models.ManyToManyField(Utilisateur, related_name='conversations')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# Groupe de discussion
class Groupe(models.Model):
    nom = models.CharField(max_length=100)
    createur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    membres = models.ManyToManyField(Utilisateur, related_name='groupes')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


# Message (texte + vocal)
class Message(models.Model):
    expediteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='messages_envoyes'
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    groupe = models.ForeignKey(
        Groupe,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    contenu = models.TextField(blank=True)
    vocal = models.FileField(upload_to='vocaux/', null=True, blank=True)

    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.expediteur}"
