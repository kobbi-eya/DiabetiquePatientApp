import json
import re
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import DoctorChangeRequest, consultations, patient, users  # Importez votre modèle utilisateur personnalisé
from .models import medecin
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

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

# Endpoint pour enregistrer le fichier PDF
@csrf_exempt
@require_http_methods(["POST"])
def save_pdf(request, id_conslt):
    consultation = get_object_or_404(consultations, idconsultations=id_conslt)
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        consultation.bilan_pdf = pdf_file
        consultation.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Veuillez fournir un fichier PDF valide.'}, status=400)

"""def send_password_email(email, password, from_email):
    subject = 'Votre mot de passe pour accéder au système'
    html_message = render_to_string('password_email.html', {'password': password})
    plain_message = strip_tags(html_message)
    to = email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)"""

@require_http_methods(["GET"])
def get_patient_info(request, patient_id):
    if request.method == 'GET': 
        try:
            # Recherchez le patient par son ID
            patient_obj = patient.objects.get(idusers=patient_id)
            
            # Serializer les données du patient si nécessaire
            patient_data = {
                'id': patient_obj.idusers,
                'nom': patient_obj.nom,
                'prenom': patient_obj.prenom,
                'sexe': patient_obj.sexe,
                'date_de_naissance': patient_obj.date_de_naissance,
                'poids': patient_obj.poids,
                'taille': patient_obj.taille,
                'mobile': patient_obj.mobile,
                'allergies': patient_obj.allergies,
                'groupe_sanguin': patient_obj.groupe_sanguin,
                'email': patient_obj.email,
                'type_diabete':patient_obj.type_diabete,
                # Ajoutez d'autres champs du modèle patient selon vos besoins
            }
            
            # Retournez les données du patient sous forme de réponse JSON
            response = JsonResponse(patient_data)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"  # Spécifiez les méthodes HTTP autorisées
            return response
            
        except patient.DoesNotExist:
            # Si le patient n'existe pas, retournez une erreur 404
            return JsonResponse({'error': 'Patient not found'}, status=404)
        except Exception as e:
            # Gérer les autres erreurs et retourner une réponse d'erreur
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['PUT', 'POST'])
def update_patient(request, patient_id):
    try:
        # Récupérer les données JSON à partir du corps de la requête
        data = json.loads(request.body.decode('utf-8'))

        # Récupérer le patient à partir de l'ID
        patients = patient.objects.get(idusers=patient_id)

        # Mettre à jour les informations du patient
        if 'taille' in data:
            patients.taille = data['taille']
        if 'allergies' in data:
            patients.allergies = data['allergies']
        if 'poids' in data:
            patients.poids = data['poids']

        # Sauvegarder les modifications dans la base de données
        patients.save()

        # Retourner une réponse JSON indiquant que la mise à jour a réussi
        return JsonResponse({"message": "Mise à jour réussie", "success": True})
    except Exception as e:
        # En cas d'erreur, retourner une réponse JSON avec un message d'erreur
        return JsonResponse({"error": str(e)}, status=500)

    
@require_http_methods(["GET"])
def get_patient_par_medecin(request, idmedId):
    if request.method == 'GET':
        try:
            
            patients = patient.objects.filter(idmed_id=idmedId)
            patients_data = [{'id': pati.idusers,
                  'nom': pati.nom,
                  'prenom': pati.prenom,
                  'sexe': pati.sexe,
                  'date_de_naissance': pati.date_de_naissance,
                  'poids': pati.poids,
                  'taille': pati.taille,
                  'mobile': pati.mobile,
                  'allergies': pati.allergies,
                  'groupe_sanguin': pati.groupe_sanguin,
                  'email': pati.email,
                  # Ajoutez d'autres champs du modèle patient selon vos besoins
                 } for pati in patients]
            print(patients_data)
            # Retournez les données sous forme de réponse JSON avec les en-têtes CORS appropriés
            response = JsonResponse({"patients": patients_data, "success": True})
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            return JsonResponse({"error": "Une erreur inattendue s'est produite."}, status=500)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)







