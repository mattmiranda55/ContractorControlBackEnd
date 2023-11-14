from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import TimeClock, Items, Employee
from .serializers import TimeClockSerializer, ItemsSerializer, EmployeeSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import jwt

#########################################
#
# Clock In/Out Views
#
#########################################
@api_view(['POST'])
def clock_in(request):
    data = json.loads(request.body)
    employee_id = data.get('employee_id')
    token = data.get('jwt')

    if not token: 
        return JsonResponse({'message': 'You are not logged in!'})
    
    current_time = datetime.now()

    # Check if employee exists
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return Response({'error': 'Employee does not exist'}, 400)

    # Create new time clock entry
    time_clock = TimeClock(employee=employee, clock_type='in', time=current_time)
    time_clock.save()

    serializer = TimeClockSerializer(time_clock)
    return Response(serializer.data)

@api_view(['POST'])
def clock_out(request):
    data = json.loads(request.body)
    employee_id = data.get('employee_id')
    token = data.get('jwt')

    if not token: 
        return JsonResponse({'message': 'You are not logged in!'})
    
    current_time = datetime.now()

    # Check if employee exists
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return Response({'error': 'Employee does not exist'}, 400)

    # Create new time clock entry
    time_clock = TimeClock(employee=employee, clock_type='out', time=current_time)
    time_clock.save()

    serializer = TimeClockSerializer(time_clock)
    return Response(serializer.data)

@api_view(['GET'])
def get_employee_time_clocks(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    employee_id = data.get('employee_id')

    if not token: 
        return JsonResponse({'message': 'You are not logged in!'})
    
        
    user = User.objects.filter(id=employee_id).first()
    
    timeclocks = TimeClock.objects.filter(employee=user.id)
    serializer = TimeClockSerializer(timeclocks, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def get_all_time_clocks(request):
    data = json.loads(request.body)
    token = data.get('jwt')

    if not token: 
        return JsonResponse({'message': 'You are not logged in!'})

    time_clocks = TimeClock.objects.all()
    serializer = TimeClockSerializer(time_clocks, many=True)
    return Response(serializer.data)

#########################################
#
# Inventory Views
#
#########################################

@api_view(['POST'])
def create_new_item(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    
    if not token: 
        return JsonResponse({'message': 'You are not logged in!'})
    
    item_name = data.get('item_name')
    item_amount = data.get('item_amount')
    item_owner = data.get('item_owner')

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
    data = json.loads(request.body)
    token = data.get('jwt')
    
    if not token: 
        return JsonResponse({'message': 'You are not logged in!'})
    
    item_id = data.get('item_id')
    item_amount = data.get('item_amount')

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
    
@api_view(['GET'])
def get_users_items(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    
    if not token: 
        return JsonResponse({'message': 'You are not logged in!'})
    
    try:
        payload = jwt.decode(token, 'CC', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid web token'}) 
        
    user = User.objects.filter(id=payload['id']).first()
    
    items = Items.objects.filter(itemOwner=user.id)
    serializer = ItemsSerializer(items, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def delete_item(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    item_id = data.get('item_id')

    if not token:
        return JsonResponse({"message": "You are not logged in!"})
    
    try:
        item = Items.objects.get(id=item_id)
    except:
        return JsonResponse({"message": "Item does not exist!"})
    
    item.delete()
    return JsonResponse({"message": "Item deleted successfully!"})

#########################################
#
# User Views
#
#########################################

@api_view(['POST'])
@csrf_exempt
def login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        return JsonResponse({'message': 'Invalid email'})
    
    if not user.check_password(password):
        return JsonResponse({'message': 'Incorrect Password'})
    
    payload = {
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=120),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, 'CC', algorithm='HS256')  # 'CC' is the secret key needed for decryption

    # frontend will store token into localstorage
    return JsonResponse({'jwt': token})       

@api_view(['POST'])
def logout(request):        
    data = json.loads(request.body)
    token = data.get('jwt')
    
    if not token:
        return JsonResponse({"message": "You are not logged in!"})

    # delete cookie from session 
    response = Response()
    response.data = {
        "message": "Successfully Logged Out"
    }
    
    return response
    
@api_view(['POST'])
def get_user_info(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    
    if not token:
        return JsonResponse({'message': 'You are not signed in'}) 

    try:
        payload = jwt.decode(token, 'CC', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid web token'}) 
    
    user = User.objects.filter(id=payload['id']).first()
    employee = Employee.objects.filter(user_id=payload['id']).first()
    user_serializer = UserSerializer(user)
    employee_serializer = EmployeeSerializer(employee)
    
    return Response([user_serializer.data, employee_serializer.data]) 

@api_view(['POST'])
def change_username(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    password = data.get('password')
    new_username = data.get('new_username')


    if not token:
        return JsonResponse({"message": "You are not logged in!"})

    try:
        payload = jwt.decode(token, 'CC', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid web token'})  
    
    user = User.objects.filter(id=payload['id']).first()

    existingUser = User.objects.filter(username=new_username).first()
    if existingUser:
        return JsonResponse({'message': 'Username already taken'})

    if user is None:
        return JsonResponse({'message': 'User not found'})
    

    # Check if the current password is correct
    if authenticate(username=user.username, password=password):
        user.username = new_username 
        user.email = new_username
        user.save()
        return JsonResponse({'message': 'Username changed successfully'}, status=200)
    else:
        return JsonResponse({'message': 'User info is incorrect'}, status=400)

@api_view(['POST'])
def change_password(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    password = data.get('password')
    new_password = data.get('new_password')


    if not token:
        return JsonResponse({"message": "You are not logged in!"})

    # validating jwt token
    try:
        payload = jwt.decode(token, 'CC', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid web token'})  
    
    user = User.objects.filter(id=payload['id']).first()

    if user is None:
        return JsonResponse({'message': 'User not found'})
    

    # Check if the current password is correct
    if authenticate(username=user.username, password=password):
        user.set_password(new_password)
        user.save()
        return JsonResponse({'message': 'Password changed successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Current password is incorrect'}, status=400)
    
@api_view(['POST'])
def register(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    existingUser = User.objects.filter(email=email).first()

    if existingUser:
        return JsonResponse({'message': 'Email already taken'}, status=505)
    
    user = User(email=email, username=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()

    payload = {
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=120),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, 'CC', algorithm='HS256')  

    return JsonResponse({'jwt': token, 'message': 'User created successfully'}, status=200)


@api_view(['POST'])
def add_employee_info(request):
    data = json.loads(request.body)
    token = data.get('jwt')
    pay_rate = data.get('pay_rate')
    position = data.get('position')

    if not token:
        return JsonResponse({"message": "You are not logged in!"})
    
    try:
        payload = jwt.decode(token, 'CC', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Invalid web token'})
    
    user = User.objects.filter(id=payload['id']).first()
    
    if not user:
        return JsonResponse({'message': 'User not found'})
    
    employee = Employee(user=user, pay_rate=pay_rate, position=position)
    employee.save()
    return JsonResponse({'message': 'Employee info added successfully'}, status=200)