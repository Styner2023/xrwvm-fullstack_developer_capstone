"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp.views import logout_request, get_dealerships, get_dealer_details, get_dealer_reviews
from djangoapp import views  # import the views from djangoapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="Home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('djangoapp/', include('djangoapp.urls')),

    # Add new patterns here  
    path('logout/', logout_request),
    path('dealerships/', get_dealerships),
    path('dealers/<int:dealer_id>/', get_dealer_details),
    path('dealers/<int:dealer_id>/reviews/', get_dealer_reviews),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
