from django.urls import path
from .views import Entreprise_list, Entreprise_detail, Entreprise_delete, EntrepriseCreateView, EntrepriseUpdateView

app_name = "entreprise"

urlpatterns = [
    path('', Entreprise_list.as_view(), name='index'),
    path('entreprise_list/', Entreprise_list.as_view(), name='entreprise_list'),
    path('entreprise_detail/<int:pk>/', Entreprise_detail.as_view(), name='entreprise_detail'),
    path('entreprise_delete/<int:pk>/', Entreprise_delete.as_view(), name='entreprise_delete'),
    path('entreprise_create/', EntrepriseCreateView.as_view(), name='entreprise_create'),
    path('entreprise_update/<int:pk>/', EntrepriseUpdateView.as_view(), name='entreprise_update'),
]
