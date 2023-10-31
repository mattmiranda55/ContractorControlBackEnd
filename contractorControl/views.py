from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import TimeClock, Employee, Items
from .serializers import TimeClockSerializer, ItemsSerializer
from django.contrib.auth.models import User


@api_view(['POST'])
def clock_in(request):
    employee_id = request.data.get('employee_id')
    current_time = datetime.now()

    # Check if employee exists
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return Response({'error': 'Employee does not exist'}, 505)

    # Create new time clock entry
    time_clock = TimeClock(employee=employee.id, clock_type='in', time=current_time)
    time_clock.save()

    serializer = TimeClockSerializer(time_clock)
    return Response(serializer.data, 400)

@api_view(['POST'])
def clock_out(request):
    employee_id = request.data.get('employee_id')
    current_time = datetime.now()

    # Check if employee exists
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return Response({'error': 'Employee does not exist'}, 505)

    # Create new time clock entry
    time_clock = TimeClock(employee=employee.id, clock_type='out', time=current_time)
    time_clock.save()

    serializer = TimeClockSerializer(time_clock)
    return Response(serializer.data, 400)

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

@api_view(['POST'])
def create_new_item(request):
    item_name = request.data.get('item_name')
    item_amount = request.data.get('item_amount')
    item_owner = request.data.get('item_owner')

    # Check if item owner exists
    try:
        owner = User.objects.get(id=item_owner)
    except User.DoesNotExist:
        return Response({'error': 'User ID does not exist'})

    # Create new item
    item = Items(itemName=item_name, itemAmount=item_amount, itemOwner=owner)
    item.save()

    serializer = ItemsSerializer(item)
    return Response(serializer.data)

@api_view(['POST'])
def update_item_quantity(request):
    item_id = request.data.get('item_id')
    item_amount = request.data.get('item_amount')

    # Check if item exists
    try:
        item = Items.objects.get(id=item_id)
    except Items.DoesNotExist:
        return Response({'error': 'Item does not exist'})
    
    if item_amount == 0:
        item.delete()
        return Response({'success': 'Item deleted'})
    else:
        # Update item quantity
        item.itemAmount = item_amount
        item.save()

        serializer = ItemsSerializer(item)
        return Response(serializer.data)
