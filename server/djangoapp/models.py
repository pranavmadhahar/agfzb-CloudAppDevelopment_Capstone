from django.db import models
from django.utils.timezone import now
from django.core import serializers
import datetime
import uuid
import json


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name
               
    


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'suv'),
        (WAGON, 'wagon')
    ]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    id = models.IntegerField(default=1, primary_key=True)
    car_type = models.CharField(max_length=50, choices=CAR_TYPES)
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.name + " " + "Make: "+ str(self.make)
               
               

    
# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name



# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:
    def __init__(self, dealership, purchase, purchase_date, name, review, car_make, car_model, car_year, id, sentiment):
        self.dealership=dealership
        self.purchase=purchase
        self.purchase_date=purchase_date
        self.name=name
        self.review=review
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.id=id
        self.sentiment=sentiment
    
    def __str__(self):
        return "Review: " + self.review 
