from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register('location', api.LocationViewSet)


from . import views
urlpatterns = [
    url(r'^api/v1/', include(router.urls)),

]


