from django.db.models import ProtectedError
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Entreprise
from .forms import EntrepriseForm

# Create your views here.
class Entreprise_list(ListView):
    model = Entreprise
    template_name = 'entreprise/list.html'
    context_object_name = 'liste'

class Entreprise_detail(DetailView):
    model = Entreprise
    template_name = 'entreprise/details.html'
    context_object_name = 'entreprise'

class Entreprise_delete(DeleteView):
    model = Entreprise
    template_name = 'entreprise/delete.html'
    context_object_name = 'entreprise'
    success_url = reverse_lazy('entreprise:entreprise_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            return self.render_to_response(self.get_context_data(
                erreur="Suppression impossible : des offres sont liées à cet élément."))

class EntrepriseCreateView(CreateView):
    model = Entreprise
    template_name = 'entreprise/form.html'
    form_class = EntrepriseForm
    success_url = reverse_lazy('entreprise:entreprise_list')

class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    template_name = 'entreprise/form.html'
    form_class = EntrepriseForm
    success_url = reverse_lazy('entreprise:entreprise_list')
