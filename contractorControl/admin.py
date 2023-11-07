from django.contrib import admin
from .models import Items, TimeClock, Employee

admin.site.register(Items)
admin.site.register(TimeClock)
admin.site.register(Employee)