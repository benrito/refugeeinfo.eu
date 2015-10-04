from django.conf.urls import include, url

from . import views



urlpatterns = [
    url(r'^location-best-guess/', views.location_best_guess),
    url(r'^', views.index),

]
