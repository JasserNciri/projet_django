from django.urls import path
from .views import Vehicule_list, Vehicule_detail, Vehicule_delete, VehiculeCreateView, VehiculeUpdateView

app_name = "vehicule"

urlpatterns = [
    path('', Vehicule_list.as_view(), name='index'),
    path('vehicule_list/', Vehicule_list.as_view(), name='vehicule_list'),
    path('vehicule_detail/<int:pk>/', Vehicule_detail.as_view(), name='vehicule_detail'),
    path('vehicule_delete/<int:pk>/', Vehicule_delete.as_view(), name='vehicule_delete'),
    path('vehicule_create/', VehiculeCreateView.as_view(), name='vehicule_create'),
    path('vehicule_update/<int:pk>/', VehiculeUpdateView.as_view(), name='vehicule_update'),
]
