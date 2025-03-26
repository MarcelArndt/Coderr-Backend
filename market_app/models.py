from django.db import models
from django.contrib.auth.models import User
import os

BUSINESSTYPE_CHOICES = [
    ("business", "Business"),
    ("customer", "Customer")
    ]

def user_directory_path(instance, filename ):
    new_filename = "profil_picture" + os.path.splitext(filename)[1]
    return os.path.join('uploads', instance.user.username, new_filename)

class Profiles(models.Model):
    user = models.OneToOneField(User, verbose_name=("User"), on_delete=models.CASCADE, related_name="inner_user")
    type = models.CharField(choices=BUSINESSTYPE_CHOICES, default="customer", max_length=10)
    location = models.CharField(max_length=50, blank=True)
    file = models.FileField(upload_to=user_directory_path, max_length=150)
    tel = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=30, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_file_path = None
            current_user_instance = Profiles.objects.filter(pk=self.pk).first()
            if current_user_instance.file:
                old_file_path = current_user_instance.file.path
            if old_file_path and os.path.exists(old_file_path):
                 os.remove(old_file_path)
        super(Profiles, self).save(*args, **kwargs)