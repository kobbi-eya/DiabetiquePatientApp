"""from rest_framework import serializers
from django.contrib.auth import authenticate

from .users import users

class UserLoginSerializer(serializers.Serializer):
 
        email = serializers.EmailField()
        password = serializers.CharField()"""

from rest_framework import serializers
from .models import consultations

class ConsultationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = consultations
        fields = '__all__'
