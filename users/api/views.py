from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from users.api.serializers import RegistrationSerializer, AccountPropertiesSerializer, ChangePasswordSerializer
from users.models import MyUser
from rest_framework.authtoken.models import Token


# Register
# Response: https://gist.github.com/mitchtabian/c13c41fa0f51b304d7638b7bac7cb694
# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        phone_number = request.data.get('phone_number', '0')
        if validate_phone_number(phone_number) is not None:
            data['error_message'] = 'این شماره تلفن همراه برای حساب دیگری استفاده شده است'
            data['response'] = 'خطا'
            return Response(data)

        email = request.data.get('email', '0').lower
        if validate_email(email) is not None:
            data['error_message'] = 'این ایمیل برای حساب دیگری استفاده شده است'
            data['response'] = 'خطا'
            return Response(data)

        username = request.data.get('username', '0')
        if validate_username(username) is not None:
            data['error_message'] = 'این نام کاربری برای حساب دیگری استفاده شده است'
            data['response'] = 'خطا'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'حساب با موفقیت ثبت شد'
            data['phone_number'] = account.phone_number
            data['email'] = account.email
            data['username'] = account.username
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['pk'] = account.pk
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


def validate_phone_number(phone_number):
    account = None
    try:
        account = MyUser.objects.get(phone_number=phone_number)
    except MyUser.DoesNotExist:
        return None
    if account is not None:
        return phone_number


def validate_email(email):
    account = None
    try:
        account = MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        return None
    if account is not None:
        return email


def validate_username(username):
    account = None
    try:
        account = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        return None
    if account is not None:
        return username


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
    try:
        account = request.user
    except MyUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except MyUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'اطلاعات حساب شما بروزرسانی شد'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        phone_number = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(phone_number=phone_number, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'خوش آمدید'
            context['pk'] = account.pk
            context['phone_number'] = phone_number
            context['token'] = token.key
        else:
            context['response'] = 'خطا'
            context['error_message'] = 'شماره تلفن همراه یا گذرواژه شده صحیح نمیباشد'

        return Response(context)


@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):

    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            account = MyUser.objects.get(email=email)
            data['response'] = email
        except MyUser.DoesNotExist:
            data['response'] = "حسابی با این ایمیل وجود ندارد"
        return Response(data)


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = MyUser
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["گذرواژه قدیمی"]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            new_password = serializer.data.get("گذرواژه جدید")
            confirm_new_password = serializer.data.get("تایید گذرواژه جدید")
            if new_password != confirm_new_password:
                return Response({"new_password": ["گذرواژهای جدید باید یکسان باشند"]},
                                status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"response": "گذرواژه شما با موفقیت بروزرسانی شد"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
