from django.urls import path
from . import views

urlpatterns = [
    
    path('list_data/', views.getData, name="getData"),
    path('add_values/', views.addValues, name="addValues"),
    path('add_device/', views.addDevice, name="addDevice")

]