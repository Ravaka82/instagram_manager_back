import json
from django.shortcuts import render
from django.http import JsonResponse
from users.core.user_service import UserService
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from users.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def inscription(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user_service = UserService()
        user = user_service.register_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=serializer.validated_data['password']
        )
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_service = UserService()
        user = user_service.authenticate_user(username, password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'Login successful',
                'id': user.id,
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            return JsonResponse({'message': 'Invalid login'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)