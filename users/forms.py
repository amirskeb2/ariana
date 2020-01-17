from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import MyUser


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(label='شماره تلفن همراه', max_length=15, help_text='')
    email = forms.EmailField(label='ایمیل', max_length=60, help_text='')
    first_name = forms.CharField(label='نام', max_length=25, help_text='')
    last_name = forms.CharField(label='نام خانوادگی', max_length=25, help_text='')

    class Meta:
        model = MyUser
        fields = ('phone_number', 'email', 'first_name', 'last_name', 'username', 'password1', 'password2')

    def clean_phone_number(self):
        if self.is_valid():
            phone_number = self.cleaned_data['phone_number']
            try:
                account = MyUser.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)
            except MyUser.DoesNotExist:
                return phone_number
            raise forms.ValidationError('این شماره تلفن همراه برای حساب دیگری استفاده شده است')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            try:
                account = MyUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except MyUser.DoesNotExist:
                return email
            raise forms.ValidationError('ااین ایمیل برای حساب دیگری استفاده شده است')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = MyUser.objects.exclude(pk=self.instance.pk).get(username=username)
            except MyUser.DoesNotExist:
                return username
            raise forms.ValidationError('این نام کاربری برای حساب دیگری استفاده شده است')

    def clean_first_name(self):
        if self.is_valid():
            first_name = self.cleaned_data['first_name']
            return first_name

    def clean_last_name(self):
        if self.is_valid():
            last_name = self.cleaned_data['last_name']
            return last_name


class MyUserAuthenticationForm(forms.ModelForm):
    phone_number = forms.CharField(label='شماره تلفن همراه', max_length=15,)
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'password')

    def clean(self):
        if self.is_valid():
            phone_number = self.cleaned_data['phone_number']
            password = self.cleaned_data['password']
            if not authenticate(phone_number=phone_number, password=password):
                raise forms.ValidationError('شماره تلفن همراه یا گذرواژه شده صحیح نمیباشد')


class AccountUpdateForm(forms.ModelForm):
    profile_pic = forms.ImageField(label='تصویر پروفایل', help_text='')
    phone_number = forms.CharField(label='شماره تلفن همراه', max_length=15, help_text='')
    email = forms.EmailField(label='ایمیل', max_length=60, help_text='')
    first_name = forms.CharField(label='نام', max_length=25, help_text='')
    last_name = forms.CharField(label='نام خانوادگی', max_length=25, help_text='')
    username = forms.CharField(label='نام کاربری', max_length=30, help_text='')

    class Meta:
        model = MyUser
        fields = ('profile_pic', 'phone_number', 'email', 'first_name', 'last_name', 'username',)

    def clean_profile_pic(self):
        if self.is_valid():
            profile_pic = self.cleaned_data['profile_pic']
            return profile_pic

    def clean_phone_number(self):
        if self.is_valid():
            phone_number = self.cleaned_data['phone_number']
            try:
                account = MyUser.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)
            except MyUser.DoesNotExist:
                return phone_number
            raise forms.ValidationError('این شماره تلفن همراه برای حساب دیگری استفاده شده است')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            try:
                account = MyUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except MyUser.DoesNotExist:
                return email
            raise forms.ValidationError('ااین ایمیل برای حساب دیگری استفاده شده است')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = MyUser.objects.exclude(pk=self.instance.pk).get(username=username)
            except MyUser.DoesNotExist:
                return username
            raise forms.ValidationError('این نام کاربری برای حساب دیگری استفاده شده است')

    def clean_first_name(self):
        if self.is_valid():
            first_name = self.cleaned_data['first_name']
            return first_name

    def clean_last_name(self):
        if self.is_valid():
            last_name = self.cleaned_data['last_name']
            return last_name
