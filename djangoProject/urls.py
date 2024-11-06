"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# djangoProject/urls.py

from django.contrib import admin
from django.urls import path, include
from finance.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Path to the home page
    path('expenses/', include('finance.urls')),  # Include finance expenses URL
    path('incomes/', include('finance.urls')),  # Include finance incomes URL
    path('accounts/', include('accounts.urls')), # Include accounts URL
]



