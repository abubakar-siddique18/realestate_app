from django.db import models
from django.db.models import Count

from django.contrib.auth.models import User


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=7, decimal_places=2)
    nearby_hospitals = models.CharField(max_length=255)
    nearby_colleges = models.CharField(max_length=255)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    likes = models.ManyToManyField(User, related_name='property_likes', blank=True)

    def __str__(self):
        return self.title
