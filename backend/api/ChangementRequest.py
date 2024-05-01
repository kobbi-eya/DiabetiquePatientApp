import json
from .serializers import DoctorChangeRequestSerializer 
from .models import consultations, medecin, patient
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import DoctorChangeRequest
from django.db.models import Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import DoctorChangeRequest, patient
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import DoctorChangeRequest
from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import permission_classes
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
def change_doctor_request(request, patient_id):
    if request.method == 'POST':
        try:
            print("google")
            data = json.loads(request.body.decode('utf-8'))
            new_doctor_email = data.get('newDoctorEmail')
            patient_instance = patient.objects.get(idusers=patient_id)
            
            # Vérifier si l'e-mail correspond à un médecin existant dans la base de données
            print(new_doctor_email)
            new_doctor = medecin.objects.filter(email=new_doctor_email).first()
            print(new_doctor)
            if not new_doctor:
                return JsonResponse({'error': 'Le médecin spécifié n\'existe pas dans la base de données'}, status=400)
            print("microsoft")
            # Créer une nouvelle instance de DoctorChangeRequest
            doctor_change_request = DoctorChangeRequest.objects.create(
                patient=patient_instance,
                new_doctor=new_doctor
            )

           # doctor_change_request.save()

            # Sérialiser la demande de changement de médecin
            serializer = DoctorChangeRequestSerializer(doctor_change_request)

            # Retourner une réponse avec les détails de la demande créée
            return JsonResponse(serializer.data)
        except patient.DoesNotExist:
            return JsonResponse({'error': 'Patient non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)



@permission_classes([permissions.IsAuthenticated])
@require_http_methods(["GET"])
def get_pending_change_requests(request, medecin_id):
    if request.method == 'GET':
        try:
            # Récupérer les demandes de changement de médecin pour le médecin spécifié
            pending_requests = DoctorChangeRequest.objects.filter(new_doctor_id=medecin_id, status='PENDING')
            print(pending_requests)
            # Sérialiser les demandes de changement
            """ data = [{
                'patient': request.patient.nom,  # Remplacer 'nom' par le champ approprié pour le nom du patient
                'date_requested': request.date_requested,
                'status': request.status
            } for request in pending_requests]"""
            serializer = DoctorChangeRequestSerializer(pending_requests, many=True)
            print(serializer)

            #response = JsonResponse({'pending_requests': data})
            response =JsonResponse({'changeRequests': serializer.data})
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)


@csrf_exempt
def accept_change_request(request, request_id):
    if request.method == 'POST':
        try:
            # Retrieve the change request
            change_request = DoctorChangeRequest.objects.get(id=request_id)
            
            # Update the status to 'ACCEPTED'
            change_request.status = 'ACCEPTED'
            change_request.save()

            # Update the idmed of the patient to the new doctor
            patient = change_request.patient
            new_doctor = change_request.new_doctor
            patient.idmed = new_doctor
            patient.save()
            
            return JsonResponse({'message': 'Change request accepted successfully. Patient assigned to new doctor.'})
        except DoctorChangeRequest.DoesNotExist:
            return JsonResponse({'error': 'Change request not found.'}, status=404)
        except patient.DoesNotExist:
            return JsonResponse({'error': 'Patient not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)

@csrf_exempt
def reject_change_request(request, request_id):
  if request.method == 'POST':
    try:
        # Retrieve the change request
        change_request = DoctorChangeRequest.objects.get(id=request_id)
        
        # Update the status to 'REJECTED'
        change_request.status = 'REJECTED'
        change_request.save()
        
        return JsonResponse({'message': 'Change request rejected successfully.'})
    except DoctorChangeRequest.DoesNotExist:
        return JsonResponse({'error': 'Change request not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
  else:
        return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)


@require_http_methods(["GET"])
def get_consultations_patient_uniquement(request, patient_id):
    if request.method == 'GET':
        try:
            # Récupérer les consultations du patient spécifié avec ordonnance non vide
            patient_consultations = consultations.objects.filter(
                Q(idpat_id=patient_id) & ~Q(ordonnance='')
            )
            print(patient_consultations)
            
            # Formater les données des consultations pour le JSON
            consultations_data = [{
                'id': consult.idconsultations,
                'date_consultation': consult.date_consultation,
                'heure_consultation': consult.heure_consultation,
                'ordonnance': consult.ordonnance,
                'description': consult.description,
                'bilan': consult.bilan,
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



@require_http_methods(["GET"])
def get_change_requests_for_patient(request, patient_id):
    if request.method == 'GET':
        try:
            
            subquery = DoctorChangeRequest.objects.filter(patient_id=patient_id).values('new_doctor_id').annotate(max_id=Max('id')).values('max_id')
            change_requests = DoctorChangeRequest.objects.filter(id__in=subquery)
            data = [{'id': request.id, 
                     'newDoctorEmail': request.new_doctor.email,
                     'newDoctorNom': request.new_doctor.nom,
                     'newDoctorPrenom': request.new_doctor.prenom,
                     'newDoctorSpeciality':request.new_doctor.specialite,
                     'status': request.status, 
                     'newDoctorMobile': request.new_doctor.mobile} for request in change_requests]
            # Répondre avec les données JSON
            response = JsonResponse(data, safe=False)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"  # Spécifiez les méthodes HTTP autorisées
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
