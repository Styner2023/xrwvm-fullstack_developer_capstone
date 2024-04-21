from django.contrib import admin
from .models import CarMake, CarModel, Dealership

# Register your models here. 

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'year']
    
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

class DealershipModelAdmin(admin.ModelAdmin):
    model = Dealership
    list_display = ['name', 'address']

# Register models here  
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Dealership, DealershipModelAdmin)
