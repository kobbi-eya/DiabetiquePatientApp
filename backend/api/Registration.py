import json
import re
from django.contrib.auth import authenticate, login
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import DoctorChangeRequest, consultations, patient, users  # Importez votre modèle utilisateur personnalisé
from .models import medecin



@csrf_exempt
def register_medecin(request):
    if request.method == 'POST':
        try:
            # Récupérer les données envoyées par le formulaire React
            data = json.loads(request.body.decode('utf-8'))
            
            # Extraire les données du formulaire
            nom = data.get('nom')
            prenom = data.get('prenom')
            date_de_naissance = data.get('date_de_naissance')
            specialite = data.get('specialite')
            mobile = data.get('mobile')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            print("Received data:", data)
            # Vérifiez que toutes les données requises sont fournies
            if not all([nom, prenom, date_de_naissance, specialite, mobile, email, password, confirm_password]):
                return JsonResponse({"error": "Veuillez fournir tous les champs requis."}, status=400)

            # Vérifiez si les mots de passe correspondent
            if password != confirm_password:
                return JsonResponse({"error": "Les mots de passe ne correspondent pas."}, status=400)

            # Vérifiez si l'email existe déjà dans la base de données
            if medecin.objects.filter(email=email).exists():
                return JsonResponse({"error": "Cet email est déjà utilisé."}, status=400)

            # Créez un nouvel objet médecin
            medecin_obj = medecin.objects.create(
                nom=nom, 
                prenom=prenom, 
                date_de_naissance=date_de_naissance, 
                specialite=specialite, 
                mobile=mobile, 
                email=email,
                role='MEDECIN'
            )
            # Vous pouvez également définir le mot de passe ici si nécessaire
            medecin_obj.set_password(password)
            medecin_obj.save()

            return JsonResponse({'redirect': '/login',"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        # Si la requête n'est pas de type POST, retournez une erreur
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import medecin
#from .serializers import MedecinSerializer
from django.http import JsonResponse

"""@csrf_exempt
def register_medecin(request):
    if request.method == 'POST':
        serializer = MedecinSerializer(data=request.data)
        if serializer.is_valid():
            # Vérifier si l'email existe déjà
            email = serializer.validated_data['email']
            if medecin.objects.filter(email=email).exists():
                return JsonResponse({'errors': {'email': 'Cet email est déjà utilisé par un autre médecin.'}}, status=400)
            
            # Vérifier si les mots de passe correspondent
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            if password != confirm_password:
                return JsonResponse({'errors': {'password': 'Les mots de passe ne correspondent pas.'}}, status=400)
            
            # Créer le médecin s'il n'y a pas d'erreurs
            medecin_obj = medecin.objects.create(
                nom=serializer.validated_data['nom'], 
                prenom=serializer.validated_data['prenom'], 
                date_de_naissance=serializer.validated_data['date_de_naissance'], 
                specialite=serializer.validated_data['specialite'], 
                mobile=serializer.validated_data['mobile'], 
                email=email,
                role='MEDECIN'
            )
            medecin_obj.set_password(password)
            medecin_obj.save()
            
            return JsonResponse({'redirect': '/login', "success": True})
        else:
            # Renvoyer les erreurs de validation sous forme de JsonResponse
            return JsonResponse({'errors': serializer.errors}, status=400)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)"""


@csrf_exempt
def register_patient_by_medecin(request, idmedId):
    if request.method == 'POST':
        try:
            medecin_obj = medecin.objects.get(idusers=idmedId)
            data = json.loads(request.body.decode('utf-8'))
            
            nom = data.get('nom')
            prenom = data.get('prenom')
            sexe = data.get('sexe')
            poids = data.get('poids')
            taille = data.get('taille')
            mobile = data.get('mobile')
            allergies = data.get('allergies')
            groupe_sanguin = data.get('groupe_sanguin')
            date_de_naissance = data.get('date_de_naissance')
            email = data.get('email')
            password = data.get('password')
            type_diabete = data.get('type_diabete')
            confirm_password = data.get('confirm_password')
            
            if not all([nom, prenom, poids, taille, mobile, allergies, sexe, groupe_sanguin, date_de_naissance, email, password]):
                return JsonResponse({"error": "Veuillez fournir tous les champs requis."}, status=400)

            if patient.objects.filter(email=email).exists():
                return JsonResponse({"error": "Cette adresse e-mail est déjà utilisée par un autre patient."}, status=400)
            
            if password != confirm_password:
                return JsonResponse({"error": "Les mots de passe ne correspondent pas."}, status=400)

            # Créer un nouvel utilisateur patient en utilisant create_user de CustomUserManager
            new_patient = patient.objects.create_user(
                email=email,
                password=password,
                nom=nom,
                prenom=prenom,
                poids=poids,
                taille=taille,
                mobile=mobile,
                allergies=allergies,
                groupe_sanguin=groupe_sanguin,
                date_de_naissance=date_de_naissance,
                role='PATIENT',
                type_diabete=type_diabete,
                sexe=sexe,
                idmed_id=idmedId
            )
            # Vous n'avez pas besoin d'appeler set_password explicitement car il est déjà appelé dans create_user
           # send_email_to_patient(email, password,medecin_obj.email,medecin_obj.password),
            return JsonResponse({'redirect': '/home_medecin', "success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
