from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Expedition

# Create your views here.
def home(request):
    return HttpResponse("<h1>welcome to ...</h1>")

def welcome(request, name):
    return HttpResponse(f"<h1>Welcome, {name}!</h1>")

def listExpeditions(request):
    expeditions = Expedition.objects.all()
    return render(request, 'expedition/list.html', {"liste": expeditions})

def detailExpedition(request, reference):
    expedition = get_object_or_404(Expedition, reference=reference)
    return render(request, 'expedition/details.html', {"expedition": expedition})

def deleteExpedition(request, reference):
    expedition = get_object_or_404(Expedition, reference=reference)
    if request.method == "POST":
        expedition.delete()
        return redirect('expedition:list')
    return render(request, 'expedition/delete.html', {"expedition": expedition})
