# Django views.py

import json
import re
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import patient, users  # Importez votre modèle utilisateur personnalisé
from .models import medecin


def validate_password(password):
    """
    Valide si le mot de passe respecte les critères suivants :
    - Au moins 8 caractères
    - Contient au moins un caractère spécial
    - Contient au moins une lettre majuscule
    """
    if len(password) < 8:
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True

#user =get_user_model
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("Received data:", data)  # Message de débogage : Afficher les données reçues depuis la requête POST
            email = data.get('email')
            password = data.get('password')
            if email and password:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    id_medecin = user.idusers
                    print("User role:", user.role)
                    login(request, user)
                    print("User authenticated:", user.email)  # Message de débogage : Afficher le nom d'utilisateur authentifié
                    if user.role == 'MEDECIN':
                        return JsonResponse({'redirect': '/home_medecin', 'role':'MEDECIN','idmed_id': id_medecin})
                    elif user.role == 'PATIENT':
                        return JsonResponse({'redirect': '/home_patient', 'role':'PATIENT'})
                else:
                    print("Authentication failed for email:", email)  # Message de débogage : Indiquer que l'authentification a échoué
                    return HttpResponseForbidden("Invalid credentials")
            else:
                return JsonResponse({"error": "Email and password are required."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)
    else:
        print("GET method received, POST method expected.")  # Message de débogage : Indiquer que la méthode GET a été reçue
        return JsonResponse({"message": "GET method is not allowed. Please use POST method forPlease use POST method for user login."}, status=405)




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
    



@csrf_exempt
def register_patient_by_medecin(request):
    #id_medecin = request.session.get('id_medecin')
    if request.method == 'POST':
        try:
            
            
            print("hello")
            # Assurez-vous que l'utilisateur est un médecin
            #if request.user.role != 'MEDECIN':
              # return JsonResponse({"error": "Méthode non autorisée"}, status=405)
            data = json.loads(request.body.decode('utf-8'))
            
            # Extraire les données du patient du JSON
            idmed_id = data.get('idmed_id')
            nom = data.get('nom')
            prenom = data.get('prenom')
            sexe =data.get('sexe')
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
            print("Received data:", data)
            # Vérifier que toutes les données requises sont fournies
            if not all([nom, prenom, poids, taille, mobile, allergies,sexe, groupe_sanguin, date_de_naissance, email, password]):
                return JsonResponse({"error": "Veuillez fournir tous les champs requis."}, status=400)

            # Vérifier si l'email existe déjà dans la base de données
            if patient.objects.filter(email=email).exists():
                return JsonResponse({"error": "Cette adresse e-mail est déjà utilisée."}, status=400)
            
            if password != confirm_password:
                return JsonResponse({"error": "Les mots de passe ne correspondent pas."}, status=400)
           

            # Créer un nouvel utilisateur patient
            new_patient = patient.objects.create(
                nom=nom,
                prenom=prenom,
                poids=poids,
                taille=taille,
                mobile=mobile,
                allergies=allergies,
                groupe_sanguin=groupe_sanguin,
                date_de_naissance=date_de_naissance,
                email=email,
                #password=make_password(password),
                role='PATIENT',
                type_diabete=type_diabete ,
                sexe =sexe ,
                idmed_id=idmed_id
                
            )
            new_patient.set_password(password)
            new_patient .save()

            return JsonResponse({'redirect': '/home_medecin', "success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
   
        
