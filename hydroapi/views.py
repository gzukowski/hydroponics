from django.contrib.auth import authenticate
from rest_framework import status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import HydroponicSystem, Measurement
from .serializers import UserSerializer, HydroponicSystemSerializer, MeasurementSerializer
from .filters import MeasurementFilter


class RegisterView(APIView):
    """
    API view for user registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request for user registration.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request for user login and token creation.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class HydroView(APIView):
    """
    API view for managing HydroponicSystem instances.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['timestamp', 'ph', 'temperature', 'tds']

    def post(self, request):
        """
        Handle POST request to create a new HydroponicSystem instance.
        """
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = HydroponicSystemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'hydroponic_system': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Handle GET request to retrieve user's HydroponicSystem instances.
        """
        response = HydroponicSystem.objects.filter(owner=request.user.id)
        serializer = HydroponicSystemSerializer(response, many=True)
        return Response({"message": "Successfully retrieved", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        Handle DELETE request to delete a HydroponicSystem instance.
        """
        try:
            hydroponic_system = HydroponicSystem.objects.get(id=id)
            if hydroponic_system.owner != request.user:
                return Response({"error": "You are not an owner."}, status=status.HTTP_403_FORBIDDEN)
            hydroponic_system.delete()
            return Response({"message": "Hydroponic system deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except HydroponicSystem.DoesNotExist:
            return Response({"error": "Hydroponic system not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        """
        Handle PUT request to update a HydroponicSystem instance.
        """
        new_name = request.data.get('name')
        try:
            hydroponic_system = HydroponicSystem.objects.get(id=id)
            if hydroponic_system.owner != request.user:
                return Response({"error": "You are not an owner."}, status=status.HTTP_403_FORBIDDEN)
            data = {'name': new_name}
            serializer = HydroponicSystemSerializer(hydroponic_system, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HydroponicSystem.DoesNotExist:
            return Response({"error": "Hydroponic system not found."}, status=status.HTTP_404_NOT_FOUND)


class MeasurementPagination(PageNumberPagination):
    """
    Custom pagination class for measurements.
    """
    page_size = 5


class MeasurementView(APIView):
    """
    API view for managing Measurement instances.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        """
        Handle POST request to create a new Measurement instance.
        """
        try:
            hydroponic_system = HydroponicSystem.objects.get(id=id)
        except HydroponicSystem.DoesNotExist:
            return Response({"error": "Hydroponic system not found."}, status=status.HTTP_404_NOT_FOUND)
        if hydroponic_system.owner != request.user:
            return Response({"error": "You are not an owner."}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['hydroponic_system'] = hydroponic_system.id
        serializer = MeasurementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'measurement': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        """
        Handle GET request to retrieve Measurement instances for a HydroponicSystem.
        """
        try:
            hydroponic_system = HydroponicSystem.objects.get(id=id)
        except HydroponicSystem.DoesNotExist:
            return Response({"error": "Hydroponic system not found."}, status=status.HTTP_404_NOT_FOUND)
        if hydroponic_system.owner != request.user:
            return Response({"error": "You are not an owner."}, status=status.HTTP_403_FORBIDDEN)
        measurements = Measurement.objects.filter(hydroponic_system=id)
        filterset = MeasurementFilter(request.GET, queryset=measurements)
        measurements = filterset.qs
        ordering = request.GET.get('ordering', None)
        if ordering:
            measurements = measurements.order_by(ordering)
        paginator = MeasurementPagination()
        paginated_measurements = paginator.paginate_queryset(measurements, request)
        serializer = MeasurementSerializer(paginated_measurements, many=True)
        return paginator.get_paginated_response(serializer.data)
