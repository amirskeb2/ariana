from rest_framework import serializers

from users.models import MyUser


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(label='شماره تلفن همراه', max_length=15)
    password2 = serializers.CharField(style={'input type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = MyUser(
            phone_number=self.validated_data['phone_number'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password and password2 and password != password2:
            raise serializers.ValidationError({'گذرواژه ها باید یکسان باشند'})
        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['pk', 'profile_pic', 'phone_number', 'email', 'first_name', 'last_name', 'username']


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(label='گذرواژه قدیمی', required=True)
    new_password = serializers.CharField(label='گذرواژه جدید', required=True)
    confirm_new_password = serializers.CharField(label='تایید گذرواژه جدید', required=True)
