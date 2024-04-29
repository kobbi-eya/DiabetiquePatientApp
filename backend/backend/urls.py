from django.contrib import admin
from django.urls import path,include
#from api.views import UserLoginAPI
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from api.views import accept_change_request, change_doctor_request, create_rendez_vous, delete_consultation, get_change_requests_for_patient, get_consultation_detail, get_consultations_patient, get_consultations_patient_uniquement, get_patient_info, get_patient_par_medecin, get_pending_change_requests, register_medecin, register_patient_by_medecin, reject_change_request, rendez_vous_medecin, rendez_vous_patient, save_pdf, update_consultation, update_patient, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
  #  path("api/user/login/", UserLoginAPI.as_view(),name="login"),
    path("api/token/", TokenObtainPairView.as_view() ,name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view() ,name="refresh"),
    path("api-auth", include("rest_framework.urls")),
    path("api/user/login/", user_login , name='user_login'),
    path("api/user/register/", register_medecin , name='register_medecin'),
    path('api/user/patientReg/<int:idmedId>',register_patient_by_medecin, name='register_patient_by_medecin'),  
    path('api/user/createRv/<int:idmedId>', create_rendez_vous , name='create_rendez_vous'),
    path('api/medecin/rendez-vous/<int:idmed_id>/', rendez_vous_medecin, name='rendez_vous_medecin'),
    path('api/patients/<int:patient_id>/', get_patient_info, name='get_patient_info'),
    path('api/patients/update/<int:patient_id>/', update_patient, name='update_patient'),
    path('api/medecin/ListesPatients/<int:idmedId>/', get_patient_par_medecin, name='get_patient_par_medecin'),
    path('api/consultations/<int:patient_id>/', get_consultations_patient, name='get_consultations_patient'),
    path('api/get/consultations/<int:id_conslt>/',get_consultation_detail, name='get_consultation_detail'),
    path('api/update/consultations/<int:id_conslt>/',update_consultation, name='update_consultation'),
    path('api/save/pdf/<int:id_conslt>/', save_pdf, name='save_pdf'),
    path('api/delete/consultations/<int:id_conslt>/',delete_consultation,name='delete_consultation'),
    path('api/patients/change_doctor/<int:patient_id>/',change_doctor_request,name='change_doctor_request'),
    path('api/doctor/change_requests/<int:medecin_id>/',get_pending_change_requests,name='get_pending_change_requests'),
    path('api/doctor/change_requests/<int:request_id>/accept/',accept_change_request,name='accept_change_request'),
    path('api/doctor/change_requests/<int:request_id>/reject/',reject_change_request,name='reject_change_request'),
    #path('api/conslt/Pat/<int:patient_id>/',get_consultations_patient_uniquement,name='get_consultations_patient_uniquement'),
    path('api/patients/affichage/change_doctor/<int:patient_id>/',get_change_requests_for_patient,name='get_change_requests_for_patient'),
   # path('send-test-email/', send_test_email, name='send_test_email'),
    path('api/rendez-vous-patient/<int:patient_id>/', rendez_vous_patient, name='rendez_vous_patient'),
    path('', include('api.urls')),
]
# backend/urls.py