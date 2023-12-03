from rest_framework import serializers
from .models import Verify, Referal


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify
        fields = ('phone_number', 'otp_code', 'is_verify', 'user')


class ReferalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referal
        fields = ('invited_user', 'referal_user', 'invite_code')
