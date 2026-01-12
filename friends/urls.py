from django.urls import path
from .views import (
    ListeNonAmisView,
    ListeAmisView,
    EnvoyerDemandeView,
    AnnulerDemandeView,
    ListeDemandesRecuesView,
    ListeDemandesEnvoyeesView,
    RepondreDemandeView,
    ListeAmisChatView
)

urlpatterns = [
    path("friends/amis/non/", ListeNonAmisView.as_view(), name="liste_non_amis"),
    path("friends/amis/", ListeAmisView.as_view(), name="liste_amis"),
    path("friends/send/", EnvoyerDemandeView.as_view(), name="envoyer_demande"),
    path("friends/demandes/annuler/", AnnulerDemandeView.as_view(), name="annuler_demande"),
    path("friends/demandes/recues/", ListeDemandesRecuesView.as_view(), name="demandes_recues"),
    path("friends/demandes/envoyees/", ListeDemandesEnvoyeesView.as_view(), name="demandes_envoyees"),
    path("friends/demandes/repondre/", RepondreDemandeView.as_view(), name="repondre_demande"),
     path("friends/utilisateurs/", ListeAmisChatView.as_view()),
]
