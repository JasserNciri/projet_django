from django.urls import path
from .views import Offre_list, Offre_detail, Offre_delete, OffreCreateView, OffreUpdateView

app_name = "offre"

urlpatterns = [
    path('', Offre_list.as_view(), name='index'),
    path('offre_list/', Offre_list.as_view(), name='offre_list'),
    path('offre_detail/<int:pk>/', Offre_detail.as_view(), name='offre_detail'),
    path('offre_delete/<int:pk>/', Offre_delete.as_view(), name='offre_delete'),
    path('offre_create/', OffreCreateView.as_view(), name='offre_create'),
    path('offre_update/<int:pk>/', OffreUpdateView.as_view(), name='offre_update'),
]
