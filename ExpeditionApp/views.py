from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Expedition
from .forms import ExpeditionForm

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

class Expedition_list(ListView):
    model = Expedition
    template_name = 'expedition/list.html'
    context_object_name = 'liste'

class Expedition_detail(DetailView):
    model = Expedition
    template_name = 'expedition/details.html'
    context_object_name = 'expedition'

class Expedition_delete(DeleteView):
    model = Expedition
    template_name = 'expedition/delete.html'
    context_object_name = 'expedition'
    success_url = reverse_lazy('expedition:list')

class ExpeditionCreateView(CreateView):
    model = Expedition
    template_name = 'expedition/form.html'
    form_class = ExpeditionForm
    success_url = reverse_lazy('expedition:list')

class ExpeditionUpdateView(UpdateView):
    model = Expedition
    template_name = 'expedition/form.html'
    form_class = ExpeditionForm
    success_url = reverse_lazy('expedition:list')
