from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name, username, password=None):
        # what to say if the user didn't fill the fields
        if not phone_number:
            raise ValueError('وارد نمودن شماره تلفن همراه الزامیست')
        if not email:
            raise ValueError('وارد نمودن ایمیل الزامیست')
        if not first_name:
            raise ValueError('وارد نمودن نام الزامیست')
        if not last_name:
            raise ValueError('وارد نمودن نام خانوادگی الزامیست')
        if not username:
            raise ValueError('وارد نمودن نام کاربری الزامیست')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name, username, password=None):
        # what to say if the user didn't fill the fields
        if not phone_number:
            raise ValueError('وارد نمودن شماره تلفن همراه الزامیست')
        if not email:
            raise ValueError('وارد نمودن ایمیل الزامیست')
        if not first_name:
            raise ValueError('وارد نمودن نام الزامیست')
        if not last_name:
            raise ValueError('وارد نمودن نام خانوادگی الزامیست')
        if not username:
            raise ValueError('وارد نمودن نام کاربری الزامیست')

        user = self.create_user(
            phone_number=phone_number,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    profile_pic = models.ImageField(verbose_name='تصویر پروفایل', default='defaulprofilepic.png',
                                    upload_to='profile_pics', blank=True)
    phone_number = models.CharField(verbose_name='شماره تلفن همراه', max_length=15, unique=True)
    email = models.EmailField(verbose_name='ایمیل', max_length=60, unique=True)
    first_name = models.CharField(verbose_name='نام', max_length=25, blank=False)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=25, blank=False)
    username = models.CharField(verbose_name='نام کاربری', max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='تاریخ ملحق شدن', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='آخرین ورود', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'

    USERNAME_FIELD = 'phone_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username',]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
