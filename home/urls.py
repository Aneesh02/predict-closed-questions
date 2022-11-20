from django.urls import path
from home import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("landing", views.landing, name="landing"),
    path("home", views.home, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
    
]
