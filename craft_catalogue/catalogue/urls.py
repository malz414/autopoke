"""
URL configuration for craft_catalogue project.

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
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import logout_view
from . import views
from .views import item_list, item_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('pokemon/<slug:pokemon_slug>/', views.pokemon_detail, name='pokemon_detail'),
    path('item/<slug:item_slug>/', views.item_detail, name='item_detail'),
    path('synergies/<slug:slug>/', views.synergy_detail_json, name='synergy_detail_json'),
    path('installation/', views.installation, name='installation'),
    
    # HTML view for synergy details (if needed elsewhere)
    path('synergy/<slug:slug>/', views.synergy_detail, name='synergy_detail'),

    path('pokemon/', views.pokemon_list, name='pokemon_list'),
    path('items/', views.item_list, name='item_list'),
    path('items/<slug:slug>/', item_detail, name='item_detail'),
    path('synergies/', views.synergy_list, name='synergy_list'),

]