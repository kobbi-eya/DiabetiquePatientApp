from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#from api.views import UserLoginAPI
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from api.authentification import user_login
from api.Registration import register_medecin, register_patient_by_medecin
from api.ChangementRequest import accept_change_request, change_doctor_request, get_change_requests_for_patient, get_pending_change_requests,  reject_change_request
urlpatterns = [
    path('admin/', admin.site.urls),
  #  path("api/user/login/", UserLoginAPI.as_view(),name="login"),
    path("api/token/", TokenObtainPairView.as_view() ,name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view() ,name="refresh"),
    path("api-auth", include("rest_framework.urls")),
    path("api/user/login/", user_login , name='user_login'),
    path("api/user/register/", register_medecin , name='register_medecin'),
    path('', include('api.urls')),
]
# backend/urls.py
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)