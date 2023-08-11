from django.urls import path, include
from .views import RegisterAPIView, VerifyOtpAPIView, LoginWithMobileView

urlpatterns = [
    path("login_mobile/", LoginWithMobileView.as_view(), name="login_user_with_mobile"),
    path("registration/", RegisterAPIView.as_view(), name="account_signup"),
    path("verify-otp/", VerifyOtpAPIView.as_view(), name="verify_otp"),
]