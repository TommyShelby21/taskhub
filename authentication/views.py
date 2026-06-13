import string

from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from system.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from django.conf import settings
import random
from system.models import Team, TeamMember


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        User.objects.create_user(
            username=serializer.validated_data['email'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        return Response({"message": "User created successfully"}, status=201)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    password = request.data.get('password')
    username = request.data.get('username')

    user = authenticate(username=username, password=password)
    if user is not None:
        response = Response()

        refresh = RefreshToken.for_user(user)

        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,         # nastav na True, pokud máš HTTPS (doporučeno)
            samesite='Lax',
            max_age=15 * 60      # 15 minut platnost tokenu
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,         # nastav na True, pokud máš HTTPS (doporučeno)
            samesite='Lax',
            max_age=7 * 24 * 60 * 60    # 7 dní platnost refresh tokenu
        )
        response.data = {
            'user': UserSerializer(user).data,
            'message': 'Login successful',
        }

        return response

    return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def logout(request):
    response = Response()

    response.delete_cookie(
        key='access_token',
        path='/',
        domain=None,
    )
    response.delete_cookie(
        key='refresh_token',
        path='/',
        domain=None,
    )

    response.data = {
        'message': 'Logout successful',
    }

    return response


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_demo(request):
    username = "demo_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    password = "".join(random.choices(string.ascii_letters + string.digits, k=10))

    user = User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password=password
    )

    team = Team.objects.create(
        name="demo".join(random.choices(string.ascii_letters + string.digits, k=5))
    )

    TeamMember.objects.create(
        user=user,
        leader=True,
        team=team
    )

    user = authenticate(username=username, password=password)

    response = Response()

    refresh = RefreshToken.for_user(user)

    response.set_cookie(
        key='access_token',
        value=str(refresh.access_token),
        httponly=True,
        secure=False,         # nastav na True, pokud máš HTTPS (doporučeno)
        samesite='Lax',
        max_age=15 * 60      # 15 minut platnost tokenu
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,         # nastav na True, pokud máš HTTPS (doporučeno)
        samesite='Lax',
        max_age=7 * 24 * 60 * 60    # 7 dní platnost refresh tokenu
    )

    response.data = { # Add data about the user
        'user': UserSerializer(user).data,
        'message': 'Demo account created successfully',
    }

    return response


@api_view(['POST'])
@authentication_classes([])  # vypneme autentizaci
@permission_classes([AllowAny])
def refresh_token(request):
    print("refresh token request")

    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'No refresh token'}, status=400)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response = Response({'message': 'Token refreshed'})
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=15* 60
        )
        return response

    except TokenError as e:
        return Response({'error': 'Invalid refresh token'}, status=401)
