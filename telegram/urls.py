
from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'receive-telegram/(?P<token>\d+)/$', views.receive_telegram),
]
