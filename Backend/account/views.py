from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,VerifyOtpSerializer,LoginSerializer,ForgotPasswordSerializer,ResetPasswordSerializer
from .models import UserData,UserToken
from rest_framework import serializers
from .email import send_otp_via_email,send_forgot_password_mail
from django.contrib.auth import login
from .utils import get_tokens_for_user,authenticate_user
import uuid
from django.utils import timezone



# Create your views here.
class SignupApiView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data["email"])
                
                return Response({
                    'status': 200,
                    'message': 'Registration successful. Check your email for further instructions.',
                    'data': serializer.data,
                })
            else:
                # If serializer is not valid, return validation error response
                return Response({
                    'status': 400,
                    'message': 'Validation error',
                    'data': serializer.errors,
                })

        except Exception as e:
            print(e)    
            return Response({
                'status': 500,
                'message': 'Something went wrong',
            })
        

class SignupVerifyOtp(APIView):
    def post(self,request):
        try:
            serializer = VerifyOtpSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email=serializer.data["email"]
                otp=serializer.data["otp"]

                user = UserData.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status' : 400,
                        'msg' : 'something went worng',
                        'data' : 'Invalid email'
                    })
                
                if user[0].otp != otp:
                    return Response({
                        'status' : 400,
                        'msg' : 'something went worng',
                        'data' : 'Wrong otp'
                    })
                user = user.first()
                user.is_verified = True
                user.save()
                return Response({
                    'status': 200,
                    'msg': 'OTP verification successful',
                    'data': 'User verified successfully'
                })
            
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Something went wrong',
            })



class LoginApi(APIView):
    def post(self,request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email=request.data['email']
                password=request.data['password']
                print(f'email:{email},password:{password}')
                user, error_msg = authenticate_user(request, email=email, password=password)
                print(user)
                if user:
                    # Authentication successful, proceed with login
                    if "@" not in email and not user.is_verified:
                        return Response({'status': 400, 'msg': 'Invalid credentials'})
                    login(request, user)
                    token = get_tokens_for_user(user)
                    return Response({
                        'status': 200,
                        'msg': 'Login successful',
                        'data': serializer.data,
                        'token': token,
                        'user_id': user.id
                    })
                else:
                    # Authentication failed, return appropriate error response
                    return Response({
                        'status': 400,
                        'msg': error_msg
                    })

        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'msg': 'Internal server error'
            })
                
        
        
class ForgotPassword(APIView):
    def post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not UserData.objects.filter(email=request.data['email']).first():
                return Response({
                    'status':400,
                    'msg': "User not found in this email"
                })
            user_obj = UserData.objects.get(email=request.data['email'])
            token = str(uuid.uuid4())
            reset_token = UserToken.objects.create(
                user=user_obj,
                token=token,
                
            )

            send_forgot_password_mail(user_obj.email,token)
            return Response({
                'status':200,
                'msg':'An email is sent'
            })
            


class ResetPassword(APIView):
    def post(self,request,token):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data['password']
                rest_token = UserToken.objects.filter(token=token,used=False).first()
                if not rest_token:
                    return Response({
                        'status': 400,
                        'msg': 'Invalid or expired token'
                    })
                user = rest_token.user
                user.set_password(password)
                user.save()

                rest_token.used = True
                rest_token.save()
                return Response({
                    'status': 200,
                    'msg': 'Password reset successful'
                })

        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'msg': 'Internal server error'
            })







        
