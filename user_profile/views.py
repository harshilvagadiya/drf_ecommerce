import uuid
from django.conf import settings
from .models import CustomUser, Address, DeactivateUser, hide_db_for_registration
from .serializers import CustomRegisterSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
def get_transactiona_id():
    unique_id = uuid.uuid4().hex
    return f"CUST/{unique_id}".upper()

class RegisterAPIView(generics.CreateAPIView):
    permission_classes= (AllowAny, )
    serializer_class = CustomRegisterSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        username = validated_data.get("username")
        email = validated_data.get("email")
        otp = validated_data.get("otp")
        phone_number = validated_data.get("phone_number")
        
        if phone_number and not email and not validated_data.get("otp"):
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                response = {"error": "Mobile number already exists"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            response = {"error": "Proceed to the next step.....of Login"}
            return Response(response, status=status.HTTP_200_OK)

        if phone_number and email and not validated_data.get("otp"):
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                return Response({"error": "Mobile number already exists...!!!"}, status=status.HTTP_400_BAD_REQUEST)
            elif CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists...!!!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                otp = str(uuid.uuid4().int)[:6]
                request.session['OTP'] = otp
                data_save = hide_db_for_registration(phone_number=phone_number, email=email, otp=otp, username=username)
                data_save.save()

                data = hide_db_for_registration.objects.filter(phone_number=phone_number).values()

                response = {'error': 'Success', "data": data}

                return Response(response, status=status.HTTP_200_OK)

class VerifyOtpAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomRegisterSerializer

    def post(self, request):  # sourcery skip: extract-method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        phone_number = validated_data.get("phone_number")
        email = validated_data.get("email")
        username = validated_data.get("username")
        otp = validated_data.get('otp')

        if phone_number and email and username and validated_data.get("otp"):
            if hide_db_for_registration.objects.filter(phone_number=phone_number, otp=otp).exists():
                data_save = CustomUser(phone_number=phone_number, email=email, username=username, otp=otp, trxn_id=get_transactiona_id())
                data_save.save()
                data = CustomUser.objects.filter(phone_number=phone_number).values()

                user = CustomUser.objects.get(phone_number=phone_number)
                token = RefreshToken.for_user(user)
                jwt_access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                jwt_refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
                response = {
                    'error': 'Success',
                    "data": data,
                    'status code': status.HTTP_200_OK,
                    'message': 'User register successfully',
                    'access': str(token.access_token),
                    'refresh_token': str(token),
                    "access_token_life_time_in_seconds": jwt_access_token_lifetime.total_seconds(),
                    "refresh_token_life_time_in_seconds": jwt_refresh_token_lifetime.total_seconds(),
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Incorrect OTP! Please try again'}, status=status.HTTP_400_BAD_REQUEST)

    