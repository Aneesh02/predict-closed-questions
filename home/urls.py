from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("landing", views.landing, name="landing"),
    path("login", views.loginUser, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path("register", views.registerUser, name="register"),
    path("process", views.process, name="process"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("project/<str:pk>/", views.viewProject, name="project"),
]
