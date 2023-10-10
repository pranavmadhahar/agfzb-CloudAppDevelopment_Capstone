from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 6

# CarModelAdmin class

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'car_type', 'year']
    search_field = ['name', 'car_type']
    list_filter = ['id']
    search_fields = ['name']


# CarMakeAdmin class with CarModelInline

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    search_fields = ['name']

# Register models here

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
