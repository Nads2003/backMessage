from django.db import models
from accounts.models import Utilisateur

class DemandeAmi(models.Model):
    expediteur = models.ForeignKey(
        Utilisateur,
        related_name='demandes_envoyees',
        on_delete=models.CASCADE
    )
    destinataire = models.ForeignKey(
        Utilisateur,
        related_name='demandes_recues',
        on_delete=models.CASCADE
    )
    accepte = models.BooleanField(default=False)
    date_demande = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('expediteur', 'destinataire')

    def __str__(self):
        return f"{self.expediteur} → {self.destinataire}"
