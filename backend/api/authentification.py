import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import  patient # Importez votre modèle utilisateur personnalisé
from .models import medecin, users 
from rest_framework_simplejwt.tokens import RefreshToken

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
                    id_patient= user.idusers
                    print("User role:", user.role)
                    login(request, user)
                    print("User authenticated:", user.email)  # Message de débogage : Afficher le nom d'utilisateur authentifié
                    if user.role == 'MEDECIN':
                        return JsonResponse({'redirect': '/login/home_medecin/', 'role':'MEDECIN','idmed_id': id_medecin})
                    elif user.role == 'PATIENT':
                        return JsonResponse({'redirect': '/home_patient', 'role':'PATIENT','id_pat':id_patient})
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


