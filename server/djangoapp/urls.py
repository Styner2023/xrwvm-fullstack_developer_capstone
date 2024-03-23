# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views  # import the views from djangoapp

app_name = 'djangoapp'
urlpatterns = [

    # path for get_cars
    path('get_cars/', views.get_cars, name='getcars'),
    # path(route='get_cars', view=views.get_cars, name ='getcars'),

    # path for registration
    path('register/', views.registration, name='register'),

    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for logout
    path('logout/', views.logout_request, name='logout'),

    # path for dealer reviews view
    # Uncomment the following line and replace `dealer_reviews_view` with the actual view function
    # path('dealer_reviews/', views.dealer_reviews_view, name='dealer_reviews'),

    # path for add a review view
    # Uncomment the following line and replace `add_review_view` with the actual view function
    # path('add_review/', views.add_review_view, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
