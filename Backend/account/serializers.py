from rest_framework import serializers
from .models import UserData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['name','email','password','is_verified']

    

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get("password"):
            raise serializers.ValidationError({"password": "Please enter password"})
        return data
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True,min_length=6)
    confirm_password = serializers.CharField(write_only=True,min_length=6)

    def validate(self,data):
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError('password doesnot match')
        
        return data        
         