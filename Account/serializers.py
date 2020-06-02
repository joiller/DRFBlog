from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        exclude = []


class BlogUserRegisterSerializer(serializers.ModelSerializer):

    # password = serializers.CharField(
    #     max_length=100,
    #     required=True,
    #     style={
    #         'input_type': 'password',
    #         'placeholder': 'PWD'
    #     }
    # )
    password2 = serializers.CharField(
        max_length=100,
        required=True,
        style={
            'input_type': 'password',
            'placeholder': 'PWD2'
        },
        write_only=True
    )

    # password2 = serializers.SerializerMethodField()

    # def get_password2(self, val):
    #     return ''

    class Meta:
        model = BlogUser
        fields = [
            'username',
            'email',
            'nickname',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def create(self, validated_data):
    #     print('ahahaha')

    def save(self, **kwargs):
        del self.validated_data['password2']
        account = BlogUser(**self.validated_data)
        account.is_active = False
        account.source = 'Register'
        print(account.password,'before')
        account.password = make_password(self.validated_data['password'],hasher='md5')
        print(account.password,'later')
        account.save()
        print(account)
        return account


class BlogUserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = [
            'username',
            'password'
        ]
