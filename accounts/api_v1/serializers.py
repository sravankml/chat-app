
from base.handlers.base_handler import ErrorMessages
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers


class GetOrUpdateUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        password1 = data['password1']
        password2 = data['password2']
        if password1 != password2:
            raise serializers.ValidationError(
                ErrorMessages.PASSWORD_MISMATCH)
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'], email=validated_data.get(
                    'email'),
                password=validated_data['password1'])
        except IntegrityError as e:
            print(e)
            raise serializers.ValidationError(
                ErrorMessages.DUPLICATE_USER)
        return user
