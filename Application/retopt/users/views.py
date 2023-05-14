from django.shortcuts import render

# Create your views here.
import random

from django.shortcuts import render
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from .email import send_otp_via_email
from .models import User, OTP
from .serializers import UserSerializer, SuperuserSerializer, RegisterUserSerializer, UpdateUserSerializer, ResetPasswordSendEmailSerializer, \
    PasswordConfirmSerializer, AccountActiveSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model, authenticate
from .permissions import UserPermission
from .renderers import UserRenderer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from .utils import Util


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (UserPermission,)
    lookup_field = 'id'
    renderer_classes = [UserRenderer, ]
    default_serializer_class = UserSerializer
    serializer_classes = {
        'list': UserSerializer,
        'create': RegisterUserSerializer,
        'retrieve': UserSerializer,
        'update': UpdateUserSerializer,
        'partial_update': UpdateUserSerializer,
        'destroy': UserSerializer
    }


    # @action(detail=False, methods=['post'])
    # def create_superuser(self, request):
    #     serializer = SuperUserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get Serializer for specific action
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    # Get Permissions for specific action
    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = [AllowAny, ]
    #     elif self.action == 'list':
    #         self.permission_classes = [IsAdminUser, ]
    #     else:
    #         self.permission_classes = [IsAuthenticated, ]
    #     return [permission() for permission in self.permission_classes]

    # override
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = RegisterUserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                try:
                    print('HI')
                    serializer.save()
                    #  OTP Code Generation
                    user = User.objects.get(email=serializer.data.get('email'))
                    otp = random.randint(100000, 999999)
                    account_activation = OTP.objects.create(user=user, code=otp, task_type='active')
                    print(account_activation.code)

                    # link Generation
                    email = serializer.data.get('email')
                    umail = urlsafe_base64_encode(force_bytes(email))
                    link = 'http://127.0.0.1:8000/api/v1/account_active_reset/' + umail
                    print(link)
                    # send_otp_via_email(user.email, account_activation)
                    body = f'Otp Code: {otp}, Click the following link to active your account: ' + link
                    data = {
                        'subject': 'Active your Account',
                        'body': body,
                        'to_email': user.email
                    }

                    #Util.send_email(data)

                    return Response(
                        {'message': 'A OTP has been sent to your mail. Please verify that...'},
                        status=status.HTTP_201_CREATED)
                except Exception as e:
                    error = f'Server Error: {e}'
                    return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'User has been deleted!'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance):
        instance.delete()


class TokenPairView(APIView):
    renderer_classes = [UserRenderer]

    # permission_classes = (AllowAny,)
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'otp': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Any keyword, will be searched in task name, task description, '
                                                 'assignee name, product name')
        }
    ))
    def post(self, request, format=None, *args, **kwargs, ):
        try:
            serializer = UserLoginSerializer(data=request.data)
            try:
                if serializer.is_valid(raise_exception=True):
                    # analyst = serializer.data.get('is_analyst')
                    # print(analyst)
                    email = serializer.data.get('email')
                    password = serializer.data.get('password')
                    print(email)
                    print(password)
                    user = authenticate(email=email, password=password)

                    if user is not None:
                        if user.is_admin:
                            refresh = RefreshToken.for_user(user)
                            token = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
                            return Response({'token': token, 'message': 'Login Success'}, status=status.HTTP_200_OK)
                        else:   
                            try:    
                                otp_obj = OTP.objects.get(user=user, task_type='active')
                            except: 
                                print("Otp Query doesn't Exists")   
                            if otp_obj.has_used:    
                                refresh = RefreshToken.for_user(user)   
                                token = {
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                }
                                return Response({'token': token, 'message': 'Login Success'}, status=status.HTTP_200_OK)
                            else:
                                return Response({'message': "Email is not verified"}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        return Response({'message': 'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                error = f'Server Error: {e}'
                return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActiveOrResetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'otp': openapi.Schema(type=openapi.TYPE_STRING,
                                  description='Any keyword, will be searched in task name, task description, '
                                              'assignee name, product name')
        }
    ))
    def post(self, request, umail, format=None):
        try:
            serializer = AccountActiveSerializer(data=request.data, context={'umail': umail})
            try:
                if serializer.is_valid(raise_exception=True):
                    # Check wheather the response is for Activating a account or Resetting the Password
                    otp_obj = OTP.objects.get(code=serializer.data.get('otp'))
                    print(otp_obj.task_type)

                    if otp_obj.task_type == 'active':
                        return Response({'message': 'Account Created Successfully'}, status=status.HTTP_201_CREATED)
                    else:
                        link = 'http://localhost:3000/api/v1/users/reset/' + umail + '/' + str(otp_obj.code)
                        print("Password Reset Link", link)
                        return Response({'message': f'Reset Password by going to this link: {link}', },
                                        status=status.HTTP_201_CREATED)
            except Exception as e:
                error = f'Server Error: {e}'
                return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = (AllowAny,)

    def post(self, request, format=None):
        try:
            serializer = ResetPasswordSendEmailSerializer(data=request.data)
            try:
                if serializer.is_valid(raise_exception=True):
                    return Response({'message': 'Password Reset link has been send. Please check your Email'},
                                    status=status.HTTP_200_OK)

            except Exception as e:
                error = f'Server Error: {e}'
                return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordConfirmView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = (AllowAny,)

    def post(self, request, umail, otp, format=None):
        serializer = PasswordConfirmSerializer(data=request.data, context={'umail': umail, 'otp': otp})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
