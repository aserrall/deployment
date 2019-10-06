from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sexo = models.IntegerField(default=0)
    dataAniversari = models.DateTimeField(default=timezone.now)
    numTelefon = models.TextField(default=0)


class FriendShip(models.Model):
    id = models.AutoField(primary_key=True)
    user_sender = models.ForeignKey(User, related_name="friendship_sender_set", on_delete=models.CASCADE)
    user_receiver = models.ForeignKey(User, related_name="friendship_receiver_set", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "FriendShip from " + self.user_sender + " to " + self.user_receiver + \
               " - Accepted: " + str(self.accepted)
