from django.db import models
from users.models import CustomUser  # CustomUser model from users app


class Verify(models.Model):
    phone_number = models.CharField(max_length=9)
    otp_code = models.CharField(max_length=4)
    is_verify = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,  null=True,on_delete=models.CASCADE)
    last_sent_time = models.DateTimeField(null=True, blank=True)  # Yangi maydon qo'shildi


class Referal(models.Model):
    invited_user = models.ForeignKey(CustomUser, related_name='invited_user', null=True, on_delete=models.CASCADE)
    referal_user = models.ForeignKey(CustomUser, related_name='referal_user',  null=True, on_delete=models.CASCADE)
    invite_code = models.CharField(max_length=8)
