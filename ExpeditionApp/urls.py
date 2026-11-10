from django.urls import path
from .views import Expedition_detail, Expedition_delete, home, welcome, listExpeditions, detailExpedition, deleteExpedition, Expedition_list, ExpeditionCreateView, ExpeditionUpdateView

app_name = "expedition"

urlpatterns = [
    path('', Expedition_list.as_view(), name='index'),
    path('home/', home, name='home'),
    path('welcome/<str:name>/', welcome, name='welcome'),
    path('list/', listExpeditions, name='list'),
    path('details/<str:reference>/', detailExpedition, name='detail'),
    path('delete/<str:reference>/', deleteExpedition, name='delete'),
    path('expedition_list/', Expedition_list.as_view(), name='expedition_list'),
    path('expedition_detail/<int:pk>/', Expedition_detail.as_view(), name='expedition_detail'),
    path('expedition_delete/<int:pk>/', Expedition_delete.as_view(), name='expedition_delete'),
    path('expedition_create/', ExpeditionCreateView.as_view(), name='expedition_create'),
    path('expedition_update/<int:pk>/', ExpeditionUpdateView.as_view(), name='expedition_update'),
]

