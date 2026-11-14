from django.db.models import ProtectedError
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Vehicule
from .forms import VehiculeForm

# Create your views here.
class Vehicule_list(ListView):
    model = Vehicule
    template_name = 'vehicule/list.html'
    context_object_name = 'liste'

class Vehicule_detail(DetailView):
    model = Vehicule
    template_name = 'vehicule/details.html'
    context_object_name = 'vehicule'

class Vehicule_delete(DeleteView):
    model = Vehicule
    template_name = 'vehicule/delete.html'
    context_object_name = 'vehicule'
    success_url = reverse_lazy('vehicule:vehicule_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            return self.render_to_response(self.get_context_data(
                erreur="Suppression impossible : des offres sont liées à cet élément."))

class VehiculeCreateView(CreateView):
    model = Vehicule
    template_name = 'vehicule/form.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicule:vehicule_list')

class VehiculeUpdateView(UpdateView):
    model = Vehicule
    template_name = 'vehicule/form.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicule:vehicule_list')
