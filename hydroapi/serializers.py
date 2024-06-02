from django.contrib.auth.models import User
from rest_framework import serializers
from .models import HydroponicSystem, Measurement

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model. Handles the creation of new users.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        user = User.objects.create_user(**validated_data)
        return user

class HydroponicSystemSerializer(serializers.ModelSerializer):
    """
    Serializer for the HydroponicSystem model. Handles serialization and deserialization
    of HydroponicSystem instances.
    """
    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'created_at', 'updated_at', 'owner']

class MeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Measurement model. Handles serialization and deserialization
    of Measurement instances.
    """
    class Meta:
        model = Measurement
        fields = ['id', 'timestamp', 'ph', 'temperature', 'tds', 'hydroponic_system']
