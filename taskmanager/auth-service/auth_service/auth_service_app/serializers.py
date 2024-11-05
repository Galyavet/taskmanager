from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        user = authenticate(**credentials)

        if user:
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is deactivated')
            data = {}
            refresh = self.get_token(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return data
        else:
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')


class ProfileSerializer(serializers.ModelSerializer):
    # access_token = serializers.UUIDField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=100,
                                       required=False,
                                       default='first_name',
                                       validators=[RegexValidator(regex=r'^[A-Za-z-]+$',
                                                                  message='First name can only contain letters and '
                                                                          'hyphens.'
                                                                  )]
                                       )
    last_name = serializers.CharField(max_length=100,
                                      required=False,
                                      default='last_name',
                                      validators=[RegexValidator(regex=r'^[A-Za-z-]+$',
                                                                 message='Last name can only contain letters and '
                                                                         'hyphens.'
                                                                 )]

                                      )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields didn`t match.'})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'].split('@')[0],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
