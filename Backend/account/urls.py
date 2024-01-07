from django.urls import path
from .views import SignupApiView,SignupVerifyOtp,LoginApi,ForgotPassword,ResetPassword

urlpatterns = [
    path('signup/',SignupApiView.as_view(),name='signup'),
    path('signup-verify-otp/',SignupVerifyOtp.as_view(),name='signup-verify-otp'),
    path('login/',LoginApi.as_view(),name='login'),
    path('forgotpassword/',ForgotPassword.as_view(),name='forgotpassword'),
    path('reset-password/<token>/',ResetPassword.as_view(),name='reset-password')
]
