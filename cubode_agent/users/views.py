from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    def post(self, request):
        
        # Check if the user with the given email already exists
        if User.objects.filter(email=request.data.get('email')).exists():
            print("user exists")
            data = {
                "success": False,
                "error": "User already exists."
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        #Create a user serialiser
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                "success": True,
                "data": { 
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email
                }
            }
            return Response(data, status=status.HTTP_201_CREATED)
        
        #Handle error
        data = {
            "success": False,
            "error": serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogInAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            print("deso this")
            return Response({'success': True, 'message': 'Successfully logged in.'}, status=status.HTTP_200_OK)
        
        # If validation fails, construct an error message
        error_message = next(iter(serializer.errors.values()))[0]
        return Response({'success': False, 'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({'message': 'Please log in with your email and password.'})

class LogOutAPI(APIView):
    def post(self, request):
        # Perform sign-out by logging out the user
        logout(request)
        return Response({'status': 'signed out'}, status=status.HTTP_200_OK)
    

    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
def check_user(request):
    user_exists = User.objects.filter(username="ben.dev@cubode.com").exists()
    return Response({'exists': user_exists})