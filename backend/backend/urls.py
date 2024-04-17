from django.contrib import admin
from django.urls import path,include
#from api.views import UserLoginAPI
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from api.views import register_medecin, user_login

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
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('api.urls')),  # Incluez les URL de votre application 'api'
    path('api-auth/', include('rest_framework.urls')),  # Incluez les URL d'authentification DRF si nécessaire
    path("api/token/", TokenObtainPairView.as_view() ,name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view() ,name="refresh"),
]"""

