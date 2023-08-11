from django.urls import path, include
from .views import RegisterAPIView, VerifyOtpAPIView

urlpatterns = [
    path("registration/", RegisterAPIView.as_view(), name="account_signup"),
    path("verify-otp/", VerifyOtpAPIView.as_view(), name="verify_otp"),
]