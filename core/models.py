from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('DONOR', 'Donor'),
        ('RECEIVER', 'Receiver'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='DONOR')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    organization_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class FoodListing(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_food')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity_kg = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_time = models.DateTimeField()
    
    # NEW: Simple text-based location
    location = models.CharField(max_length=255, help_text="e.g., 123 Main St or Downtown Bakery", default="Location not specified")
    
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.quantity_kg}kg"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"