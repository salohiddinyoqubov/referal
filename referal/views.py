import random
import string
from datetime import datetime, timedelta, timezone

import requests
from rest_framework import viewsets, status
from rest_framework.response import Response

from users.models import CustomUser
from .models import Verify, Referal

from .utils import generate_otp_code, send_sms, generate_invite_code


class SendCodeViewSet(viewsets.ViewSet):
    def create(self, request):
        phone_number = request.data.get('phone_number')
        try:
            verify_instance = Verify.objects.get(phone_number=phone_number)
            print(60)
            if verify_instance.is_verify is True:
                return Response({'message': 'Phone number already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            elif verify_instance.last_sent_time and verify_instance.last_sent_time and (
                    datetime.now().replace(tzinfo=timezone.utc) - verify_instance.last_sent_time) < timedelta(
                hours=1):

                has_time = verify_instance.last_sent_time + timedelta(hours=1) - datetime.now().replace(
                    tzinfo=timezone.utc)
                return Response(
                    {'xabar': f"Keyingi kodni so'rish mumkinligi {has_time.seconds // 60} daqiqadan so'ng."},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                print(74)
                otp_code = generate_otp_code()  # Generate or retrieve OTP code here
                verify_instance.otp_code = otp_code
                verify_instance.last_sent_time = datetime.now()

                verify_instance.save()
                print(81)
                # send_sms(phone_number, otp_code)
                return Response({'otp_code': otp_code}, status=status.HTTP_200_OK)
        except Verify.DoesNotExist:
            otp_code = generate_otp_code()  # Generate OTP code here
            verify_instance = Verify.objects.create(phone_number=phone_number, otp_code=otp_code)
            send_sms(phone_number, otp_code)
            return Response({'otp_code': otp_code}, status=status.HTTP_200_OK)


class VerifyCodeViewSet(viewsets.ViewSet):
    def create(self, request):
        phone_number = request.data.get('phone_number')
        otp_code = request.data.get('otp_code')
        try:
            verify_instance = Verify.objects.get(phone_number=phone_number, otp_code=otp_code)
            if not verify_instance.is_verify:
                verify_instance.is_verify = True
                verify_instance.save()
                CustomUser.objects.create(phone_number=phone_number)
                return Response({'message': 'Phone number verified successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Phone number already verified.'}, status=status.HTTP_200_OK)

        except Verify.DoesNotExist:
            return Response({'message': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)


class ReferalViewSet(viewsets.ViewSet):
    def create(self, request):
        referal_user_phone = request.data.get('referal_user')
        invited_user_phone = request.data.get('invited_user')
        invite_code = generate_invite_code()

        if referal_user_phone and invited_user_phone:
            try:
                referal_user = CustomUser.objects.filter(phone_number=referal_user_phone).first()

                if not referal_user:
                    return Response({'message': 'Referal user not found.'}, status=status.HTTP_400_BAD_REQUEST)

                else:

                    user_create = CustomUser.objects.get_or_create(phone_number=invited_user_phone)[0]

                    is_verify = Verify.objects.filter(phone_number=user_create.phone_number).first()
                    if not is_verify:
                        invited_user_verify = Verify.objects.create(phone_number=user_create.phone_number,
                                                                otp_code=invite_code, user=user_create)


                        referal = Referal.objects.create(invited_user=user_create, referal_user=referal_user,
                                                         invite_code=invite_code)
                        if invited_user_verify.last_sent_time and invited_user_verify.last_sent_time and (
                                datetime.now().replace(
                                    tzinfo=timezone.utc) - invited_user_verify.last_sent_time) < timedelta(
                            hours=1):
                            has_time = invited_user_verify.last_sent_time + timedelta(hours=1) - datetime.now().replace(
                                tzinfo=timezone.utc)
                            return Response(
                                {'xabar': f"Keyingi kodni so'rish mumkinligi {has_time.seconds // 60} daqiqadan so'ng."},
                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            invited_user_verify.last_sent_time = datetime.now()
                            invited_user_verify.save()
                            send_sms(invited_user_phone, invite_code)
                    elif is_verify and not is_verify.is_verify:

                        return Response({'message': 'User found but not is verify'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'message': 'User already exists!!.'}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'invite_code': invite_code}, status=status.HTTP_201_CREATED)
            except CustomUser.DoesNotExist:
                return Response({'message': 'Referal user not found.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'Params is empty.'}, status=status.HTTP_400_BAD_REQUEST)


class ReferalConfirmViewSet(viewsets.ViewSet):
    def create(self, request):
        invited_user_phone = request.data.get('invited_user')
        invite_code = request.data.get('invite_code')
        try:
            invited_user_verify = Verify.objects.get(phone_number=invited_user_phone, otp_code=invite_code)
            invited_user = CustomUser.objects.filter(phone_number=invited_user_phone).first()
            if invited_user:
                invited_user_verify.is_verify = True
                invited_user_verify.save()
                return Response({'message': 'User already verified.'}, status=status.HTTP_200_OK)
            else:
                CustomUser.objects.create(phone_number=invited_user_phone)
                invited_user_verify.is_verify = True
                invited_user_verify.save()
                return Response({'message': 'User verified and created successfully.'}, status=status.HTTP_200_OK)
        except (Verify.DoesNotExist, CustomUser.DoesNotExist):
            return Response({'message': 'Invalid information provided.'}, status=status.HTTP_400_BAD_REQUEST)
