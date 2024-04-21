# Django views.py

import json
import re
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseForbidden
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

 
