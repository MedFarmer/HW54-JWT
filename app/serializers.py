from rest_framework import serializers
from django.contrib.auth.models import AbstractUser
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']
        
    def validate(self, data):        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user    
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')        
