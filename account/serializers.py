from rest_framework import serializers
from .models import *
from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=4, required=True, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm")

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop("password_confirm")
        if password != password_confirm:
            msg = ("Пароли не совпадают")
            raise serializers.ValidationError(msg)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code, status="register")
        return user


class CreateNewPasswordSerialier(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь не найден."
            )
        return email

    def validate_code(self, code):
        if not User.objects.filter(
                activation_code=code,
                is_active=False
        ).exists():
            raise serializers.ValidationError(
                "Неверный код активации"
            )
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            msg = ("Пароли не совпадают")
            raise serializers.ValidationError(msg)
        return attrs

    def save(self, **kwargs):
        validated_data = self.validated_data
        email = validated_data.get("email")
        code = validated_data.get("email")
        password = validated_data.get("password")
        try:
            user = User.objects.get(
                email=email,
                activation_code=code,
                is_active=False
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь не найден"
            )
        user.is_active = True
        user.activation_code = ""
        user.set_password(password)
        user.save()
        return user