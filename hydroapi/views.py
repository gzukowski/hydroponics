from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, HydroponicSystemSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from .models import HydroponicSystem

class RegisterView(APIView):
    
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    
    permission_classes = [AllowAny] 
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class HydroView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = HydroponicSystemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'hydroponic_system': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        response = HydroponicSystem.objects.filter(owner=request.user.id)
        
        serializer = HydroponicSystemSerializer(response, many=True)
        
        return Response({"message": "Successfully retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            hydroponic_system = HydroponicSystem.objects.get(id=id)
            
            if hydroponic_system.owner != request.user:
                return Response({"error": "You are not an owner."}, status=status.HTTP_403_FORBIDDEN)

            hydroponic_system.delete()
            return Response({"message": "Hydroponic system deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except HydroponicSystem.DoesNotExist:
            return Response({"error": "Hydroponic system not found."}, status=status.HTTP_404_NOT_FOUND)