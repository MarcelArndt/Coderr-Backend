from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import os


### Profiles ### _______________________________________________________________________

BUSINESSTYPE_CHOICES = [
    ("business", "Business"),
    ("customer", "Customer")
    ]

PROGRESS_STATUS_CHOICES = [
    ("in_progress", "in Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled")
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
    updated_at =  models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        if self.pk:
            old_file_path = None
            current_user_instance = Profiles.objects.filter(pk=self.pk).first()
            if current_user_instance.file:
                old_file_path = current_user_instance.file.path
            if old_file_path and os.path.exists(old_file_path):
                os.remove(old_file_path)
        super(Profiles, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} | {self.type.title()}"
    

### Offers ### _______________________________________________________________________

def user_offer_directory_path(instance, filename ):
    new_filename = "offer" + os.path.splitext(filename)[1]
    return os.path.join('uploads', instance.user.user.username, new_filename)

class Offers(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False)
    image = models.FileField(upload_to=user_offer_directory_path, max_length=100, blank=True, null=True)
    description = models.TextField(blank=False)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)
    min_price =  models.CharField(max_length=120, blank=True, null=True)
    min_delivery_time = models.PositiveSmallIntegerField(blank=True, null=True)
 
class OffersDetails(models.Model):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE ,related_name="details")
    title = models.CharField(max_length=100, blank=False)
    revisions = models.IntegerField(blank=False)
    delivery_time_in_days = models.PositiveSmallIntegerField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    offer_type = models.CharField(max_length=30, blank=False)
    features = models.JSONField(blank=False, null=False)

    def __str__(self):
        return f"{self.title} | {self.created_at} | {self.user.username}"

### Orders ### _______________________________________________________________________

class Orders(models.Model):
    title = models.CharField(max_length=50)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=30)
    status = models.CharField(choices=PROGRESS_STATUS_CHOICES, max_length=30)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)

### Reviews ### _______________________________________________________________________
class Reviews(models.Model):
    business_user = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name="business_user")
    reviewer = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)


### BaseInfo ### _______________________________________________________________________
class BaseInfo(models.Model):
    review_count = models.IntegerField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    business_profile_count = models.IntegerField()
    offer_count = models.IntegerField()