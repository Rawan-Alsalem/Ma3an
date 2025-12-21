from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'System Admin'),
        ('agency', 'Tour Agency'),
        ('guide', 'Tour Guide'),
        ('traveler', 'Traveler'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    subscriptionType = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.subscriptionType
    

class TravelAgency(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    agencyName = models.CharField(max_length=255)
    licenseNumber = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    approved = models.BooleanField(default=False)
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.agencyName
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
