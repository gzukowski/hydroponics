from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import RegisterView, LoginView, HydroView, MeasurementView

urlpatterns = [
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
    path("", HydroView.as_view()),
    path("<int:id>", HydroView.as_view()),
    path("<int:id>/measurements", MeasurementView.as_view()),
]