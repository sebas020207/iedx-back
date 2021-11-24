from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import Administrator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ['id', 'name', 'last_name', 'address',
                  'phone', 'email', 'role', 'password', 'photo', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['is_active'] = True
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(
        max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(
        max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Your old password was entered incorrectly. Please enter it again.'
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(
                "The two password fields didn't match."
            )
        password_validation.validate_password(
            data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class ImageSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ['photo']
