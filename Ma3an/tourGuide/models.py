from django.db import models

# Create your models here.

from django.db import models

class Announcement(models.Model):
    tour = models.ForeignKey(
        "agency.Tour",
        on_delete=models.CASCADE,
        related_name="announcements"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
