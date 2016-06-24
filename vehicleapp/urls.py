from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/(?P<vin>[A-Z0-9]+)/$', views.api, name='api'),
]