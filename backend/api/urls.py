

# api/urls.py

from django.urls import path
#from .views import user_login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

urlpatterns = [
    #path('token/', TokenObtainPairView.as_view(), name="get_token"),
   # path('token/refresh/', TokenRefreshView.as_view(), name="refresh"),
   # path('user/login/', views.user_login, name='login'),
]



#path("api/user/register/", UserLoginAPI.as_view(),name="register"),