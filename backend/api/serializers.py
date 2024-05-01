
from .models import DoctorChangeRequest
from rest_framework import serializers
from .models import consultations

class ConsultationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = consultations
        fields = '__all__'


class DoctorChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorChangeRequest
        fields = '__all__'
