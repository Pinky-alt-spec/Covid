from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name='index'),
    path('selectCountry', views.indCountryData, name='indCountryData')

]