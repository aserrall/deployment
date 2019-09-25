from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sexo = models.IntegerField(default=0)
    dataAniversari = models.DateTimeField(default=timezone.now)
    numTelefon = models.TextField(default=0)
