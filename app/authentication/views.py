from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User, Family
from .serializers import UserSerializer, FamilySerializer
from constant.authentication import *

@api_view(['POST'])
def signup(request):
    try:
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')

        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=username)
            token = Token.objects.get(user=user)

            response_data = {'user': serializer.data, 'token': token.key}
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        response_data = {'error': serializer.errors}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        authenticate_user = authenticate(username=username, password=password)

        if authenticate_user is not None:
            user = User.objects.get(username=username)
            token, created_token = Token.objects.get_or_create(user=user)

            if token:
                response_data = {'token': token.key}
            elif created_token: 
                response_data = {'token': created_token.key}

            return Response(response_data, status=status.HTTP_202_ACCEPTED)
        
        response_data = {'error': USER_ERROR_MESSAGE}
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        if request.user:
            request.user.auth_token.delete()
            response_data = {'message': LOGOUT_SUCCESS_MESSAGE}
            return Response(response_data, status=status.HTTP_200_OK)
        
        response_data = {'error': USER_ERROR_MESSAGE}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_family(request):
    try:
        serializer = FamilySerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            serializer.create(user=user)
            family = Family.objects.get(senior_id=user.id)
            response_data = {'id': family.id, 'family': serializer.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        response_data = {'error': serializer.errors}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def join_family(request):
    try:
        serializer = UserSerializer()
        serializer.join(user=request.user, data=request.data)

        response_data = {'message': JOIN_FAMILY_SUCCESS_MESSAGE}
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]
