from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import UniqueValidator
from .models import CustomUser, Address, DeactivateUser, hide_db_for_registration
from drf_extra_fields.fields import Base64ImageField


class DeactivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeactivateUser
        exclude = ["deactive", "user"]

class CustomRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=False)
    otp = serializers.CharField(max_length=6, required=False, allow_blank=True)
    phone_number = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = hide_db_for_registration
        fields = ("id", "username", "email", "otp", "phone_number")

    def create(self, validated_data):
        user = hide_db_for_registration.objects.create(
            mobile_number=validated_data['mobile_number'],
            email=validated_data['email'],
            username=validated_data['username'],
            otp=validated_data["otp"],
        )
        user.save()
        return user