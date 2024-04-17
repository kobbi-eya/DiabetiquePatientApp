from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role, **extra_fields)

class users(AbstractBaseUser):
    idusers = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    nom = models.CharField(max_length=50, default="")
    prenom = models.CharField(max_length=50, default="")
    role_choices = [
        ('MEDECIN', 'Médecin'),
        ('PATIENT', 'Patient')
    ]
    role = models.CharField(max_length=10, choices=role_choices, default="")
    email = models.CharField(max_length=50, unique=True, default="")
    last_login = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class medecin(users):
    specialite = models.CharField(max_length=50, null=False, default="")
    mobile = models.IntegerField(null=False, default="")
    date_de_naissance = models.DateField(null=False, default="")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Récupère l'argument 'user' s'il est présent
        super().__init__(*args, **kwargs)  # Appelle le constructeur de la classe parente avec les autres arguments
        if user:
            self.user = user
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"



