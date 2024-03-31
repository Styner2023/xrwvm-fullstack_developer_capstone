# Standard library imports 
from django.db import models
from django.utils.timezone import now  
from django.core.validators import MaxValueValidator, MinValueValidator

# Local app imports
# from .models import CarMake 

# Create your models here.

# CarMake model

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation

# class CarMake(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as required
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ])
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation

class Dealership(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Review(models.Model):
    dealer = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
