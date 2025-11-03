from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=255)  # Title of the property
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)  # Location of the property
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"
