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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp.views import get_dealers, get_dealer_details, get_dealer_reviews, login_user
from djangoapp.views import get_dealerships

from djangoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="Home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('', include('djangoapp.urls')),

    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('get_dealers/', get_dealers, name='get_dealers'), 
    path('dealers/<int:dealer_id>/', get_dealer_details),
    path('dealers/<int:dealer_id>/reviews/', get_dealer_reviews),
    path('dealer/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    path('get_dealers/', lambda request: redirect('dealers/')), # Add this line
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
