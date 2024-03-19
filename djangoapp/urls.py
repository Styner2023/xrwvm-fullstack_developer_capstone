# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views  # import the views from djangoapp

app_name = 'djangoapp'
urlpatterns = [
    # path for registration
    # path('register/', views.register, name='register'),


    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for logout
    path('logout/', views.logout_request, name='logout'),

    # path for register
    path('register/', views.register, name='register'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
