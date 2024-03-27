import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel, Dealership 
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    if request.body:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('userName')
        password = data.get('password')

        if username is not None and password is not None:
            logger.info(f"Received username: {username}")
            logger.info(f"Received password: {password}")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                data = {"userName": username, "status": "Authenticated"}
                return JsonResponse(data)
            else:
                logger.warning(f"Authentication failed for username: {username}")
                data = {"status": "Failed", "message": "Invalid username or password"}
                return JsonResponse(data, status=401)
        else:
            return JsonResponse({'error': 'Missing username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Empty request body'}, status=400)

def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

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
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

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

def get_cars(request):
    if CarMake.objects.count() < 5:
        initiate()

    car_makes = CarMake.objects.all()

    cars = []
    for car_make in car_makes:
        car_models = CarModel.objects.filter(car_make=car_make)
        for car_model in car_models:
            cars.append({"CarModel": car_model.name, "CarMake": car_make.name})

    logger.info(cars)
    return JsonResponse({"CarModels":cars})

def initiate():
    car_makes = ['Toyota', 'Ford', 'Chevrolet', 'Honda', 'Nissan']

    car_models = {
        'Toyota': ['Corolla', 'Camry', 'Prius', 'Avalon', 'Yaris'],
        'Ford': ['F-150', 'Escape', 'Mustang', 'Explorer', 'Fusion'],
        'Chevrolet': ['Malibu', 'Impala', 'Camaro', 'Equinox', 'Cruze'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit'],
        'Nissan': ['Altima', 'Maxima', 'Rogue', 'Murano', 'Versa']
    }

    for make in car_makes:
        car_make, created = CarMake.objects.get_or_create(name=make)

        for model in car_models[make]:
            car_model, created = CarModel.objects.get_or_create(name=model, car_make=car_make)

def get_dealerships(request, state="All"):
    base_url = 'https://kstiner101-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai'  # Your dealership API base URL
    if(state == "All"):
        endpoint = "/get_dealers"
    else:
        # Ensure state does not start or end with a '/'
        state = state.strip('/')
        endpoint = "/get_dealers/"+state
    dealerships = get_request(base_url + endpoint)
    if dealerships is None:
        return JsonResponse({"status":500,"message":"Error fetching dealerships"})
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_reviews(request, dealer_id):
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

@csrf_exempt
def populate_database(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_makes = data.get('car_makes')
            car_models = data.get('car_models')

            for make in car_makes:
                car_make, created = CarMake.objects.get_or_create(name=make)

                for model in car_models[make]:
                    car_model, created = CarModel.objects.get_or_create(name=model, car_make=car_make)

            return JsonResponse({"message": "Database populated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return None
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP error: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"Error connecting: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        print(f"Timeout error: {errt}")
        return None

    return response.json()
