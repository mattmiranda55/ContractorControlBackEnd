from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import TimeClock, Employee
from .serializers import TimeClockSerializer
from django.contrib.auth.models import User


@api_view(['POST'])
def clock_in(request):
    employee_id = request.data.get('employee_id')
    current_time = datetime.now()

    # Check if employee exists
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return Response({'error': 'Employee does not exist'})

    # Create new time clock entry
    time_clock = TimeClock(employee=employee.id, clock_type='in', time=current_time)
    time_clock.save()

    serializer = TimeClockSerializer(time_clock)
    return Response(serializer.data)

@api_view(['POST'])
def clock_out(request):
    employee_id = request.data.get('employee_id')
    current_time = datetime.now()

    # Check if employee exists
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return Response({'error': 'Employee does not exist'})

    # Create new time clock entry
    time_clock = TimeClock(employee=employee.id, clock_type='out', time=current_time)
    time_clock.save()

    serializer = TimeClockSerializer(time_clock)
    return Response(serializer.data)

@api_view(['GET'])
def get_employee_time_clocks(request):
    employee_id = request.data.get('employee_id')

    # Check if employee exists
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return Response({'error': 'Employee does not exist'})

    time_clocks = TimeClock.objects.filter(employee=employee.id)
    serializer = TimeClockSerializer(time_clocks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_time_clocks(request):
    time_clocks = TimeClock.objects.all()
    serializer = TimeClockSerializer(time_clocks, many=True)
    return Response(serializer.data)