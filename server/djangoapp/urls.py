# Uncomment the imports before you add the code
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('get_cars/', views.get_cars, name='get_cars'),
    path('get_dealers/', views.get_dealers, name='get_dealers'),
    path('get_dealerships/', views.get_dealerships, name='get_dealerships'),
    path('get_dealerships/<str:state>/', views.get_dealerships, name='get_dealerships_by_state'),
    path('get_dealer_reviews/<int:dealer_id>/', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('get_dealer_details/<int:dealer_id>/', views.get_dealer_details, name='get_dealer_details'),
    path('add_review/', views.add_review, name='add_review'),
    path('populate_database/', views.populate_database, name='populate_database'),
    path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.registration, name='register'),
]
    # New URL patterns
    # path('dealers/', views.dealers, name='dealers'),
    # path('get_dealers_template/', views.get_dealers_template,

