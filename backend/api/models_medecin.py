"""from django.db import models
from .models import users

class medecin(users):  # Utilisez directement le modèle users
    specialite = models.CharField(max_length=50, null=False, default="")
    mobile = models.IntegerField(null=False, default="")
    date_de_naissance = models.DateField(null=False, default="")

    def __str__(self):
        return f"{self.nom} {self.prenom}"""