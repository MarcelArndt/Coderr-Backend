from django.db import models
from django.contrib.auth.models import User


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
        return "uploads/user/" + filename

class Profiles(models.Model):
    user = models.OneToOneField(User, verbose_name=("User"), on_delete=models.CASCADE, related_name="inner_user")
    type = models.CharField(choices=BUSINESSTYPE_CHOICES, default="customer", max_length=10)
    location = models.CharField(max_length=50, blank=True)
    file = models.FileField(upload_to=user_directory_path, max_length=150)
    tel = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=30, blank=True)
    updated_at =  models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return f"{self.user.username}"
    

### Offers ### _______________________________________________________________________

def user_offer_directory_path(instance, filename ):
    return "uploads/offer/" + filename

class Offers(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False)
    image = models.FileField(upload_to=user_offer_directory_path, max_length=100, blank=True, null=True)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    min_price =  models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=0)
    min_delivery_time = models.PositiveSmallIntegerField(blank=True, null=True)
 
class OffersDetails(models.Model):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE ,related_name="details")
    title = models.CharField(max_length=100, blank=False)
    revisions = models.IntegerField(blank=False)
    delivery_time_in_days = models.PositiveSmallIntegerField(blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    offer_type = models.CharField(max_length=30, blank=False)
    features = models.JSONField(blank=False, null=False)

    def __str__(self):
        return f"{self.title} | {self.offer.created_at} | {self.offer.user.user.username}"

### Orders ### _______________________________________________________________________

class Orders(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    offersDetails = models.ForeignKey(OffersDetails, on_delete=models.CASCADE ,related_name="offersDetails", default=None)
    status = models.CharField(choices=PROGRESS_STATUS_CHOICES, max_length=30)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

### Reviews ### _______________________________________________________________________

class Reviews(models.Model):
    business_user = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name="business_user")
    reviewer = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)