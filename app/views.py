from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.pop('access')
            refresh_token = response.data.pop('refresh')
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh')
        if refresh:
            request.data['refresh'] = refresh
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.pop('access')
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        return response

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access = request.COOKIES.get('access')
        if access:
            request.data['token'] = access
        return super().post(request, *args, **kwargs)    

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
