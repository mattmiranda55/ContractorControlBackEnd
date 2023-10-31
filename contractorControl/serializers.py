from rest_framework import serializers
from .models import *

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'itemName', 'itemAmount', 'itemOwner', 'last_updated']

class TimeClockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeClock
        fields = ['id', 'employee', 'clock_type', 'time']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'position', 'pay_rate']