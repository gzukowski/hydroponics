from django.contrib.auth.models import User
from rest_framework import serializers
from .models import HydroponicSystem, Measurement

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'created_at', 'updated_at', 'owner']
        
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'timestamp', 'ph', 'temperature', 'tds', 'hydroponic_system']
