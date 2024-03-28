# Uncomment the imports before you add the code
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views  # import the views from djangoapp

app_name = 'djangoapp'
urlpatterns = [
    path('get_cars/', views.get_cars, name='getcars'),
    path('register/', views.registration, name='register'),
    path(route='login', view=views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('populate_database/', views.populate_database, name='populate_database'),
    # path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

  # path for dealer reviews view
    # Uncomment the following line and replace `dealer_reviews_view` with the actual view function
    # path('dealer_reviews/', views.dealer_reviews_view, name='dealer_reviews'),

    # path for add a review view
    # Uncomment the following line and replace `add_review_view` with the actual view function
    # path('add_review/', views.add_review_view, name='add_review'),