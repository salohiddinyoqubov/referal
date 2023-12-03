import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    # username = models.CharField(unique=False, max_length=255)

    def save(self, *args, **kwargs):
        self.username = str(uuid.uuid4())
        super().save(*args, **kwargs)

