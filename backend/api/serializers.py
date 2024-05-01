
from .models import DoctorChangeRequest, medecin
from rest_framework import serializers
from .models import consultations

class ConsultationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = consultations
        fields = '__all__'

"""class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = medecin
        fields = '__all__'
        password = serializers.CharField(write_only=True)
        confirm_password = serializers.CharField(write_only=True)
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def validate_email(self, value):
        if medecin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé par un autre médecin.")
        return value """
class DoctorChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorChangeRequest
        fields = '__all__' 
