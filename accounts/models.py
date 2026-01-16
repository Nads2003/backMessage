from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    est_en_ligne = models.BooleanField(default=False)
    derniere_activite = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.username

