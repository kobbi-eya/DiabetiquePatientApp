import json
import re
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import consultations, patient, users  # Importez votre modèle utilisateur personnalisé
from .models import medecin
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    

"""def send_password_email(recipient_email, password):
    # Configuration de l'e-mail
    sender_email = "votre_email@gmail.com"  # Modifier avec votre adresse e-mail
    subject = "Votre mot de passe pour le portail du patient"
    body = f"Bonjour,\n\nVoici votre mot de passe pour accéder au portail du patient : {password}\n\nCordialement,\nVotre médecin"

    # Création du message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Ajout du corps du message
    message.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP et envoi de l'e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, 'votre_mot_de_passe')  # Modifier avec votre mot de passe
        server.send_message(message)"""      


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
            # Envoi de l'e-mail contenant le mot de passe au patient
            #send_password_email(new_patient.email,new_patient.password)
            return JsonResponse({'redirect': '/home_medecin', "success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

from datetime import datetime, timedelta           
@csrf_exempt
def create_rendez_vous(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            idmede = data.get('idmed')
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
                heure_consultation=heure_consultation
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
               interval = current_rendez_vous_datetime - rendez_vous_datetime
               if interval.total_seconds() < 0 and abs(interval.total_seconds()) < 20 * 60:
                  return JsonResponse({"error": "Il doit y avoir un intervalle de 20 minutes minimum entre les rendez-vous sur le même jour."}, status=400)




            rendez_vous = consultations.objects.create(
                idpat_id=idpat,
                idmede_id=idmede,
                date_consultation=date_consultation,
                heure_consultation=heure_consultation,
            )
            rendez_vous.save()

            return JsonResponse({'redirect': '/home_medecin',"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

 

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "OPTIONS"])
def rendez_vous_medecin(request, idmed_id):
    if request.method == 'GET':
        try:
            # Récupérer les rendez-vous (consultations) pour le médecin spécifié
            rendez_vous = consultations.objects.filter(idmede_id=idmed_id, bilan='', ordonnance='')

            # Serializer les rendez-vous si nécessaire
            rendez_vous_data = [{'id': rv.idconsultations, 'date_consultation': rv.date_consultation, 'heure_consultation': rv.heure_consultation ,'idpat': rv.idpat.idusers } for rv in rendez_vous]
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



from django.http import JsonResponse
from .models import patient

from django.http import JsonResponse
from .models import patient

from django.http import JsonResponse

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
            
            # Récupérez tous les patients associés à ce médecin
            patients = patient.objects.filter(idmed_id=idmedId)
            
            # Formatez les données des patients pour le JSON
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

"""@require_http_methods(["GET"])
def get_patient_par_medecin(request, idmed_id):
    print('1')
    if request.method == 'GET':
        try:
            print('2')
            print("Trying to retrieve doctor with ID:", idmed_id)
            # Récupérez le médecin par ID
            medecin_obj = medecin.objects.get(idusers=idmed_id)
            print('3')
            # Récupérez tous les patients associés à ce médecin
            patients = patient.objects.filter(idmed=medecin_obj)
            print('4')
            # Formatez les données des patients pour le JSON
            data = [
                {
                    "nom": p.nom,
                    "prenom": p.prenom,
                    "age": p.date_de_naissance.year,
                    "poids": p.poids,
                    "taille": p.taille,
                    "groupe_sanguin": p.groupe_sanguin,
                    "sexe": p.sexe,
                }
                for p in patients
            ]
            
            response = JsonResponse({"patients": data, "redirect": "/liste_patient", "success": True})
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET"
            response["Access-Control-Allow-Headers"] = "Content-Type"
            return response
        
        except medecin.DoesNotExist:
            print("Médecin introuvable")
            return JsonResponse({"error": "Médecin introuvable."}, status=404)
        
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return JsonResponse({"error": "Une erreur inattendue s'est produite."}, status=500)
    
    else:
        print("Invalid method")"""

from django.http import JsonResponse
from .models import patient, consultations
from django.db.models import Q

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
                                   #'medecin': f"{consult.idmede.nom} {consult.idmede.prenom}"
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



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import consultations  # Assurez-vous d'importer correctement le modèle

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
                'patient': {
                    'id': consultation.idpat.idusers,  # Inclure l'ID du patient
                    'nom': consultation.idpat.nom,  # Inclure le nom du patient
                    'prenom': consultation.idpat.prenom,  # Inclure le prénom du patient
                    'email': consultation.idpat.email  # Inclure l'email du patient, etc.
                    # Ajoutez d'autres champs du patient selon vos besoins
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
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Remplacez cette URL par celle de votre frontend
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"  # Spécifiez les méthodes HTTP autorisées
        return response




from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def import_pdf(request, consultation_id):
    consultation = get_object_or_404(consultations, pk=consultation_id)
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        # Code pour sauvegarder le fichier PDF et le traiter si nécessaire
        # Une fois le traitement terminé, vous pouvez rediriger l'utilisateur vers la page de consultation
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Veuillez fournir un fichier PDF valide.'}, status=400)