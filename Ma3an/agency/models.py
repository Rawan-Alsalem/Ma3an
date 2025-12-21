from django.db import models
from django.contrib.auth.models import User


class Agency(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TourGuide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else "No User"

    def is_available(self, start_date, end_date):
        """
        يتحقق إذا كان المرشد متاح بين تاريخين
        """
        conflicting_tours = self.tour_set.filter(
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        return not conflicting_tours.exists()


class Tour(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # هذا هو الـ Capacity
    travelers = models.PositiveIntegerField(
        help_text="Max capacity (number of travelers)"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.PositiveIntegerField(default=1)

    tour_guide = models.ForeignKey(
        TourGuide,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='tour_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class TourSchedule(models.Model):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    day_number = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity_title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location_name = models.CharField(max_length=255)
    location_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.tour.name} - Day {self.day_number}"
