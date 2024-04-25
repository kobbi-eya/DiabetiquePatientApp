from django.contrib import admin
from django.urls import path,include
#from api.views import UserLoginAPI
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from api.views import create_rendez_vous, get_consultation_detail, get_consultations_patient, get_patient_info, get_patient_par_medecin, register_medecin, register_patient_by_medecin, rendez_vous_medecin, update_consultation, update_patient, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
  #  path("api/user/login/", UserLoginAPI.as_view(),name="login"),
    path("api/token/", TokenObtainPairView.as_view() ,name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view() ,name="refresh"),
    path("api-auth", include("rest_framework.urls")),
    path("api/user/login/", user_login , name='user_login'),
    path("api/user/register/", register_medecin , name='register_medecin'),
    path('api/user/patientReg/',register_patient_by_medecin, name='register_patient_by_medecin'),  
    path('api/user/createRv/', create_rendez_vous , name='create_rendez_vous'),
    path('api/medecin/rendez-vous/<int:idmed_id>/', rendez_vous_medecin, name='rendez_vous_medecin'),
    path('api/patients/<int:patient_id>/', get_patient_info, name='get_patient_info'),
    path('api/patients/update/<int:patient_id>/', update_patient, name='update_patient'),
    path('api/medecin/ListesPatients/<int:idmedId>/', get_patient_par_medecin, name='get_patient_par_medecin'),
    path('api/consultations/<int:patient_id>/', get_consultations_patient, name='get_consultations_patient'),
    path('api/get/consultations/<int:id_conslt>/',get_consultation_detail, name='get_consultation_detail'),
    path('api/update/consultations/<int:id_conslt>/',update_consultation, name='update_consultation'),
    path('', include('api.urls')),
]
# backend/urls.py