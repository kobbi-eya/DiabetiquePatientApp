

from rest_framework import serializers
from .models import consultations

class ConsultationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = consultations
        fields = '__all__'
