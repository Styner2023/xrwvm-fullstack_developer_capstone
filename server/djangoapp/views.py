from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel, Dealership 
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    # Check if request body is not empty
    if request.body:
        try:
            # Try to load JSON data from request body
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # If error, return a response with status 400 (Bad Request)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Extract username and password from data
        username = data.get('userName')
        password = data.get('password')

        # Check if username and password are not None
        if username is not None and password is not None:
            # Log the received username and password
            logger.info(f"Received username: {username}")
            logger.info(f"Received password: {password}")

            # Try to check if provided credential can be authenticated
            user = authenticate(username=username, password=password)
            if user is not None:
                # If user is valid, call login method to login current user
                login(request, user)
                data = {"userName": username, "status": "Authenticated"}
                return JsonResponse(data)
            else:
                # Log a message if authentication failed
                logger.warning(f"Authentication failed for username: {username}")
                data = {"status": "Failed", "message": "Invalid username or password"}
                return JsonResponse(data, status=401)
        else:
            # If either username or password is None, return a response with status 400
            return JsonResponse({'error': 'Missing username or password'}, status=400)
    else:
        # If request body is empty, return a response with status 400
        return JsonResponse({'error': 'Empty request body'}, status=400)
        
        # Logout the user
def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')  # Redirect to 'home' page

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
@csrf_exempt
def registration(request):
    context = {}

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# New register view function
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/register.html', {'form': form})

# # Get an instance of a logger
# logger = logging.getLogger(__name__)

def get_cars(request):
    if CarMake.objects.count() < 5:
        initiate()

    car_makes = CarMake.objects.all()  # Get all car makes

    cars = []
    for car_make in car_makes:
        car_models = CarModel.objects.filter(car_make=car_make)  # Get all car models for this make
        for car_model in car_models:
            cars.append({"CarModel": car_model.name, "CarMake": car_make.name})

    logger.info(cars)  # Log the data
    return JsonResponse({"CarModels":cars})

def initiate():
    # Define some default car makes
    car_makes = ['Toyota', 'Ford', 'Chevrolet', 'Honda', 'Nissan']

    # Define some default car models for each car make
    car_models = {
        'Toyota': ['Corolla', 'Camry', 'Prius', 'Avalon', 'Yaris'],
        'Ford': ['F-150', 'Escape', 'Mustang', 'Explorer', 'Fusion'],
        'Chevrolet': ['Malibu', 'Impala', 'Camaro', 'Equinox', 'Cruze'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit'],
        'Nissan': ['Altima', 'Maxima', 'Rogue', 'Murano', 'Versa']
    }

    # Create the car makes and models in the database
    for make in car_makes:
        car_make, created = CarMake.objects.get_or_create(name=make)

        for model in car_models[make]:
            car_model, created = CarModel.objects.get_or_create(name=model, car_make=car_make)

def get_dealerships(request):
    dealers = Dealership.objects.all()
    data = [{"id": d.id, "name": d.name} for d in dealers] 
    return JsonResponse(data, safe=False)

def get_dealer_reviews(request, dealer_id):
    # Implement this view
    pass

def get_dealer_details(request, dealer_id):
    """Returns page with details for the given dealer"""
    
    try:
        dealer_id = int(dealer_id) 
    except ValueError:
        raise Http404()
        
    dealer = get_object_or_404(Dealership, id=dealer_id)

    context = {
        'dealer': dealer
    }

    return render(request, 'dealer_details.html', context)

def add_review(request):
    # Implement this view
    pass

@csrf_exempt
def populate_database(request):
    if request.method == 'POST':
        try:
            # Load JSON data from request body
            data = json.loads(request.body)
            # Extract car makes and models from data
            car_makes = data.get('car_makes')
            car_models = data.get('car_models')

            # Create the car makes and models in the database
            for make in car_makes:
                car_make, created = CarMake.objects.get_or_create(name=make)

                for model in car_models[make]:
                    car_model, created = CarModel.objects.get_or_create(name=model, car_make=car_make)

            return JsonResponse({"message": "Database populated successfully"})
        except json.JSONDecodeError:
            # If error, return a response with status 400 (Bad Request)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        # If request method is not POST, return a response with status 405 (Method Not Allowed)
        return JsonResponse({'error': 'Method not allowed'}, status=405)
