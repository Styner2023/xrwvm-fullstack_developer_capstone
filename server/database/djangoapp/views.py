from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from .restapis import get_request, analyze_review_sentiments, post_review
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CarMake, CarModel, Dealership
from .populate import initiate
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def login_user(request):
    if request.method == 'POST':
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
        # If request method is not POST, return a response with status 405 (Method Not Allowed)
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')  # Redirect to 'home' page

def registration(request):
    if request.method == 'POST':
        try:
            # Try to load JSON data from request body
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # If error, return a response with status 400 (Bad Request)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')

        username_exist = False
        email_exist = False

        try:
            # Check if user already exists
            User.objects.get(username=username)
            username_exist = True
        except User.DoesNotExist:
            # If not, simply log this is a new user
            logger.debug(f"{username} is a new user")

        if not username_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
            # Login the user and redirect to list page
            login(request, user)
            data = {"userName": username, "status": "Authenticated"}
            return JsonResponse(data)
        else:
            data = {"userName": username, "error": "Already Registered"}
            return JsonResponse(data)
    else:
        # If request method is not POST, return a response with status 405 (Method Not Allowed)
        return JsonResponse({'error': 'Method not allowed'}, status=405)

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

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealers(request):
    dealers = Dealership.objects.all()
    context = {"dealers": dealers}
    return render(request, 'dealers.html', context)

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

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
