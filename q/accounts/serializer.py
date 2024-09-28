from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'phone_number']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")

        if len(data['password']) < 5:
            raise serializers.ValidationError("Password must be at least 5 characters long.")

        if data['password'].isnumeric():
            raise serializers.ValidationError("Password must contain both letters and numbers.")

        return data

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

class OptCodes(serializers.Serializer):
    code = serializers.IntegerField()

class ChangeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value)
        if not user.exists():
            raise serializers.ValidationError("you not registered")
        return value

class ChangeSerializer2(serializers.Serializer):
    code = serializers.IntegerField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")

        if len(data['password']) < 5:
            raise serializers.ValidationError("Password must be at least 5 characters long.")

        if data['password'].isnumeric():
            raise serializers.ValidationError("Password must contain both letters and numbers.")

        return data