from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=30, blank=True)
