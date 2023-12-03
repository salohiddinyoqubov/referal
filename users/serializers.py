from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'password')  # Add 'phone_number' field

        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }
