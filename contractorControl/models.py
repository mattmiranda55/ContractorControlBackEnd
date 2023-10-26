from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Items(models.Model):
    itemName = models.CharField()
    itemAmount = models.IntegerField()
    itemOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(default=timezone.now, null=True, blank=True)

class TimeClock(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_type = models.CharField(max_length=3, choices=[('in', 'In'), ('out', 'Out')])
    time = models.DateTimeField(default=timezone.now, null=True, blank=True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    pay_rate = models.DecimalField(max_digits=6, decimal_places=2)

