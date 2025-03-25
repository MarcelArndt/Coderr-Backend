from django.db import models
from django.contrib.auth.models import User


BUSINESSTYPE_CHOICES = [
    ("business", "Business"),
    ("customer", "Customer")
    ]

class CustomUser(models.Model):
    user = models.ForeignKey(User, verbose_name=("User"), on_delete=models.CASCADE)
    type = models.CharField(choices=BUSINESSTYPE_CHOICES, default="customer", max_length=10)
