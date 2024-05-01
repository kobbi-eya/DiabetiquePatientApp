import json
import re
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import DoctorChangeRequest, consultations, patient, users  # Importez votre modèle utilisateur personnalisé
from .models import medecin
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import consultations  # Assurez-vous d'importer correctement le modèle
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.db.models import Q
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
@require_http_methods(["POST"])  # Utilisez POST pour la méthode HTTP
def update_consultation(request, id_conslt):
    consultation = get_object_or_404(consultations, idconsultations=id_conslt)  # Utilisez le nom correct du modèle
    if request.method == 'POST':
        # Récupérez les données du formulaire JSON envoyé dans le corps de la requête
        data = json.loads(request.body)
        # Mettez à jour les champs de la consultation avec les données fournies
        consultation.ordonnance = data.get('ordonnance', consultation.ordonnance)
        consultation.bilan = data.get('bilan', consultation.bilan)
        # Ajoutez d'autres champs à mettre à jour selon vos besoins
        
        # Enregistrez les modifications dans la base de données
        consultation.save()
        return JsonResponse({'success': True})
    else:
        response = JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"  
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"  
        return response


#create consultation = create rendezvous avec champ bilan et ordoannace null

@require_http_methods(["GET"])
def get_consultation_detail(request,id_conslt):
    if request.method == 'GET':
        try:
            consultation = get_object_or_404(consultations, pk=id_conslt)  # Utilisez le nom correct du modèle
            data = {
                'id': consultation.idconsultations,  # Assurez-vous d'utiliser les bons noms de champs
                'date': consultation.date_consultation,  # Assurez-vous d'utiliser les bons noms de champs
                'heure': consultation.heure_consultation,  # Assurez-vous d'utiliser les bons noms de champs
                'ordonnance': consultation.ordonnance,
                'bilan': consultation.bilan,
                'bilan_pdf': consultation.bilan_pdf.url if consultation.bilan_pdf else None,
                'patient': {
                'id': consultation.idpat.idusers,  # Inclure l'ID du patient
                'nom': consultation.idpat.nom,  # Inclure le nom du patient
                'prenom': consultation.idpat.prenom,  # Inclure le prénom du patient
                'email': consultation.idpat.email  # Inclure l'email du patient  # Ajoutez d'autres champs du patient selon vos besoins
                },
                'medecin': {
                'idmedecin': consultation.idmede.idusers
                }

                # Ajoutez d'autres champs selon vos besoins
            }
            response = JsonResponse(data)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)


from datetime import datetime, timedelta           
@csrf_exempt
def create_rendez_vous(request,idmedId):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            idmede = idmedId
            date_consultation = data.get('dateConsultation')
            heure_consultation = data.get('heureConsultation')
            notes = data.get('notes')
            idpat = data.get('idpat')
            print("Received data:", data)
            print("Type of idmede:", type(idmede))

            patient_obj = patient.objects.get(email=email)
            idpat = patient_obj.idusers
            print("Type of patient_obj.idmed_id:", type(patient_obj.idmed_id))
            # Convert idmede to integer
            idmede = int(idmede)

            # Vérifier que toutes les données requises sont fournies
            if not all([idmede, idpat, date_consultation, heure_consultation, notes]):
                return JsonResponse({"error": "Veuillez fournir tous les champs requis."}, status=400)

            print(idpat)
            # Vérifier si le patient associé au rendez-vous est bien celui du médecin connecté
            if patient_obj.idmed_id != idmede:
                print("patient_obj.idmed_id:", patient_obj.idmed_id)
                print("idmede:", idmede)
                return JsonResponse({"error": "Vous n'êtes pas autorisé à créer un rendez-vous pour ce patient."}, status=403)
            

            date_consultation = datetime.strptime(date_consultation, '%Y-%m-%d').date()

            # Convertir l'heure de consultation en objet datetime.time
            heure_consultation = datetime.strptime(heure_consultation, '%H:%M').time()


            # Vérifier s'il existe déjà un rendez-vous pour le même patient à la même date et à la même heure
            existing_rendez_vous_same_time = consultations.objects.filter(
                idpat=idpat,
                date_consultation=date_consultation,
                heure_consultation=heure_consultation,
                description=notes
            ).exists()
            if existing_rendez_vous_same_time:
                return JsonResponse({"error": "Ce créneau est déjà pris pour ce patient."}, status=400)
           
            # Filtrer tous les rendez-vous existants pour le même patient et la même date de consultation
            existing_rendez_vous_same_day = consultations.objects.filter(
              idpat=idpat,
              date_consultation=date_consultation,
            )

           # Vérifier l'intervalle de 20 minutes entre le nouveau rendez-vous et les rendez-vous existants sur le même jour
            current_rendez_vous_datetime = datetime.combine(date_consultation, heure_consultation)
            for rendez_vous in existing_rendez_vous_same_day:
               rendez_vous_datetime = datetime.combine(rendez_vous.date_consultation, rendez_vous.heure_consultation)
               interval = abs(current_rendez_vous_datetime - rendez_vous_datetime)
               if interval.total_seconds() < 20 * 60:
                return JsonResponse({"error": "Il doit y avoir un intervalle de 20 minutes minimum entre les rendez-vous sur le même jour."}, status=400)

            rendez_vous = consultations.objects.create(
                idpat_id=idpat,
                idmede_id=idmede,
                date_consultation=date_consultation,
                heure_consultation=heure_consultation,
                description=notes,
            )
            rendez_vous.save()

            return JsonResponse({'redirect': '/home_medecin',"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["GET"])
def get_consultations_patient(request, patient_id):
    if request.method == 'GET':
        try:
           
            # Récupérer les consultations du patient spécifié avec ordonnance non vide
            patient_consultations = consultations.objects.filter(
                Q(idpat_id=patient_id) & ~Q(ordonnance=''))
            

            # Formater les données des consultations pour le JSON
            consultations_data = [{'id': consult.idconsultations,
                                   'date_consultation': consult.date_consultation,
                                   'heure_consultation': consult.heure_consultation,
                                   'ordonnance': consult.ordonnance,
                                   'description': consult.description,
                                   'bilan': consult.bilan,
                                   'bilan_pdf': consult.bilan_pdf.url if consult.bilan_pdf else None,
                                   'medecin': f"{consult.idmede.nom} {consult.idmede.prenom}"
                                   # Ajouter d'autres champs du modèle consultation selon vos besoins
                                   } for consult in patient_consultations]
            print(consultations_data)
            # Retourner les données des consultations sous forme de réponse JSON avec les en-têtes CORS appropriés
            response = JsonResponse({"consultations": consultations_data, "success": True})
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            return JsonResponse({"error": "Une erreur inattendue s'est produite."}, status=500)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
@require_http_methods(["GET", "OPTIONS"])
def rendez_vous_patient(request, patient_id):
    if request.method == 'GET':
        try:
            # Récupérer les rendez-vous (consultations) pour le patient spécifié
            Patient = get_object_or_404(patient, idusers=patient_id)
            rendez_vous = consultations.objects.filter(idpat=patient_id, bilan='', ordonnance='')

            # Serializer les rendez-vous si nécessaire
            rendez_vous_data = [{'id': rv.idconsultations, 'date_consultation': rv.date_consultation, 'heure_consultation': rv.heure_consultation ,'idpat': rv.idpat.idusers,'idmedId':rv.idmede.idusers,'nomMedecin':rv.idmede.nom,'prenomMedecin':rv.idmede.prenom ,'mobile':rv.idmede.mobile} for rv in rendez_vous]
            print(rendez_vous_data)

            # Retourner les données sous forme de réponse JSON avec les en-têtes CORS appropriés
            response = JsonResponse({'rendez_vous': rendez_vous_data}, safe=False)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            # Gérer les erreurs et retourner une réponse d'erreur si nécessaire
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Si la méthode de requête n'est pas GET, renvoyer une réponse d'erreur
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
@require_http_methods(["GET", "OPTIONS"])
def rendez_vous_medecin(request, idmed_id):
    if request.method == 'GET':
        try:
            # Récupérer les rendez-vous (consultations) pour le médecin spécifié
            rendez_vous = consultations.objects.filter(idmede=idmed_id, bilan='', ordonnance='')

            # Serializer les rendez-vous si nécessaire
            rendez_vous_data = [{'id': rv.idconsultations, 'date_consultation': rv.date_consultation, 'heure_consultation': rv.heure_consultation ,'idpat': rv.idpat.idusers,'idmedId':rv.idmede.idusers } for rv in rendez_vous]
            print(rendez_vous_data)
            # Retourner les données sous forme de réponse JSON avec les en-têtes CORS appropriés
            response = JsonResponse({'rendez_vous': rendez_vous_data}, safe=False)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            # Gérer les erreurs et retourner une réponse d'erreur si nécessaire
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Si la méthode de requête n'est pas GET, renvoyer une réponse d'erreur
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
"""essai de minimisation du code 
@require_http_methods(["GET", "OPTIONS"])
def get_rendez_vous(request, user_id):
    if request.method == 'GET':
        try:
            user = get_object_or_404(users, id=user_id)
            role = user.role

            if role == 'MEDECIN':
                # Récupérer les rendez-vous (consultations) pour le médecin spécifié
                rendez_vous = consultations.objects.filter(idmede=user_id, bilan='', ordonnance='')
            elif role == 'PATIENT':
                # Récupérer les rendez-vous (consultations) pour le patient spécifié
                rendez_vous = consultations.objects.filter(idpat=user_id, bilan='', ordonnance='')
            else:
                return JsonResponse({'error': 'Rôle non valide'}, status=400)

            # Serializer les rendez-vous si nécessaire
            rendez_vous_data = [{'id': rv.idconsultations, 'date_consultation': rv.date_consultation, 'heure_consultation': rv.heure_consultation ,'idpat': rv.idpat.idusers,'idmedId':rv.idmede.idusers} for rv in rendez_vous]
            print(rendez_vous_data)

            # Retourner les données sous forme de réponse JSON avec les en-têtes CORS appropriés
            response = JsonResponse({'rendez_vous': rendez_vous_data}, safe=False)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            # Gérer les erreurs et retourner une réponse d'erreur si nécessaire
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Si la méthode de requête n'est pas GET, renvoyer une réponse d'erreur
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
"""
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_consultation(request, id_conslt):
    consultation = get_object_or_404(consultations, idconsultations=id_conslt)

    if request.method == "DELETE":
        consultation.delete()
        return JsonResponse({"message": "Consultation deleted successfully"})