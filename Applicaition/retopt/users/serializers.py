import random

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User, OTP
from .utils import Util


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class SuperuserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Ensure the passwords match and create a superuser with the provided email and password.
        """
        password1 = data.pop('password1')
        password2 = data.pop('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        data['is_superuser'] = True
        data['is_staff'] = True
        user = get_user_model().objects.create_user(**data, password=password1)
        return user






class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'DOB', 'gender', 'city_code', 'is_analyst', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'DOB': {'required': True} 
        }

    # validating password 1 and password2
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password Doesn't match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        # password = validate_data.pop('password', None)
        # instance = self.Meta.model(**validate_data)
        # if password is not None:
        #     instance.set_password(password)
        # instance.save()
        # return instance


class AccountActiveSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10)

    class Meta:
        fields = ['otp']

    def validate(self, attrs):
        otp = attrs.get('otp')
        umail = self.context.get('umail')
        email = smart_str(urlsafe_base64_decode(umail))
        user = User.objects.get(email=email)
        otp_obj = OTP.objects.filter(user=user).last()
        try:
            if OTP.objects.filter(code=otp).exists():
                otp_obj.has_used = True
                otp_obj.save()
                return attrs
            else:
                raise ValidationError('Your OTP is not correct')
        except Exception as e:
            raise ValidationError('OTP Validation Error:', e)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'DOB', 'gender', 'city_code']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']




class ResetPasswordSendEmailSerializer(serializers.Serializer): 
    email = serializers.EmailField(max_length=255)  

    class Meta: 
        fields = ['email']  

    def validate(self, attrs):  
        email = attrs.get('email')  
        print(email)
        print(User.objects.filter(email=email))
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            umail = urlsafe_base64_encode(force_bytes(user.email))
            #print('Encoded User Mail', umail)
            # token = PasswordResetTokenGenerator().make_token(user)
            # Generate OTP
            otp = random.randint(100000, 999999)
            reset_otp = OTP.objects.create(user=user, code=otp, task_type='reset')
            print("Password Reset OTP", reset_otp.code)
            link = 'http://localhost:3000/api/v1/users/password-reset/' + umail + '/' + str(reset_otp.code)
            print("Password Reset Link", link)

            # Send Email
            body = f'Otp Code: {otp}, Click the following link to reset your Password' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }

            #Util.send_email(data)

            return attrs
        else:
            raise ValidationError('You are not a Registered User')


class PasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            umail = self.context.get('umail')
            token = self.context.get('otp')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            email = smart_str(urlsafe_base64_decode(umail))
            user = User.objects.get(email=email)

            if not OTP.objects.filter(code=token).exists():
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
