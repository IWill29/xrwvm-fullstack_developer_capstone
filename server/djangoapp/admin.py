from django.contrib import admin
from .models import CarMake, CarModel

# 1. Šis ļauj pievienot modeļus markas lapā
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

# 2. KONFIGURĀCIJA MARKĀM (CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    # Šeit rādām laukus, kas ir CarMake modelī
    fields = ['name', 'description']
    list_display = ['name', 'description']
    # Pievienojam iespēju pievienot modeļus tieši šeit
    inlines = [CarModelInline]

# 3. KONFIGURĀCIJA MODEĻIEM (CarModel)
class CarModelAdmin(admin.ModelAdmin):
    # Šeit rādām laukus, kas ir CarModel modelī
    fields = ['car_make', 'name', 'type', 'year']
    list_display = ['name', 'car_make', 'type', 'year']

# 4. REĢISTRĀCIJA (pareizais pāris: Modelis + tā Admin konfigurācija)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
