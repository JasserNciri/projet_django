from django.urls import path
from .views import home, welcome, listExpeditions, detailExpedition, deleteExpedition

app_name = "expedition"

urlpatterns = [
    path('home/', home, name='home'),
    path('welcome/<str:name>/', welcome, name='welcome'),
    path('list/', listExpeditions, name='list'),
    path('details/<str:reference>/', detailExpedition, name='detail'),
    path('delete/<str:reference>/', deleteExpedition, name='delete'),
]
