from django.db import models
from django.contrib.auth.models import User
import uuid
from cloudinary.models import CloudinaryField


class ServiceRequest(models.Model):

    SERVICE_TYPES = (
        ("Truck", "KHASHAULER"),
        ("Dispatch rider", "KHASRIDER"),
        ("Foot courier", "KHASRUNNER"),
    )

    STATUS = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("on_the_way", "On The Way"),
        ("completed", "Completed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)

    # 📍 Locations
    pickup_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)

    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)

    drop_lat = models.FloatField(null=True, blank=True)
    drop_lng = models.FloatField(null=True, blank=True)

    distance_km = models.FloatField(null=True, blank=True)

    # 💰 Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)

    weight = models.FloatField(null=True, blank=True)

    # 📞 CONTACT DETAILS
    sender_phone_number = models.CharField(max_length=15, null=True, blank=True)

    receiver_name = models.CharField(max_length=200, default="Unknown")

    receiver_phone_number = models.CharField(max_length=15, null=True, blank=True)

    # 📦 PACKAGE
    package_description = models.CharField(max_length=255, default="Item")

    # 📦 STATUS
    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False)

    payment_status = models.BooleanField(default=False)

    # ⏱ TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True,null=True)  # 🔥 FIXED

    def __str__(self):
        return f"{self.service_type} - {self.tracking_id}"


class BusinessImage(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField("images")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
    
    
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"    
   
   
   
   
class LandingPage(models.Model):
    title = models.CharField(max_length=200, default="KHASIS EXPRESS")
    subtitle = models.CharField(max_length=300, default="Swift, Reliable Delivery Across Lagos")
    background_image = CloudinaryField("image")   # ✅ FIXED

    def __str__(self):
        return self.title