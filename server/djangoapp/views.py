from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CarMake, CarModel, Dealership
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def login_user(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('userName')
                password = data.get('password')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            username = request.POST.get('userName')
            password = request.POST.get('password')

        if username and password:
            logger.info(f"Received username: {username}")
            logger.info(f"Received password: {password}")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                logger.warning(f"Authentication failed for username: {username}")
                return JsonResponse({"status": "Failed", "message": "Invalid username or password"}, status=401)
        else:
            return JsonResponse({'error': 'Missing username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('home')
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"})
        else:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
    return JsonResponse({"CarModels": cars})

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def dealer_details(request, dealer_id):
    if dealer_id:
        dealership = get_request(f"/fetchDealer/{dealer_id}")
        reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        context = {"dealer": dealership, "reviews": reviews}
        return render(request, 'dealer_details.html', context)
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealers(request):
    dealers = get_request("/fetchDealers")
    if isinstance(dealers, list):
        current_date = timezone.now().date()
        context = {"dealers": dealers, "current_date": current_date}
        return render(request, 'dealers.html', context)
    else:
        logger.warning(f"Unexpected data format: {dealers}")
        return render(request, 'dealers.html', {"error": "Failed to fetch dealers"})

def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

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
        
        
