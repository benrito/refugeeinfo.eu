
from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'receive-telegram/(?P<token>.+)/$', views.receive_telegram),
]
