from django.db.models import ProtectedError
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Offre
from .forms import OffreForm

# Create your views here.
class Offre_list(ListView):
    model = Offre
    template_name = 'offre/list.html'
    context_object_name = 'liste'

class Offre_detail(DetailView):
    model = Offre
    template_name = 'offre/details.html'
    context_object_name = 'offre'

class Offre_delete(DeleteView):
    model = Offre
    template_name = 'offre/delete.html'
    context_object_name = 'offre'
    success_url = reverse_lazy('offre:offre_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            return self.render_to_response(self.get_context_data(
                erreur="Suppression impossible : des offres sont liées à cet élément."))

class OffreCreateView(CreateView):
    model = Offre
    template_name = 'offre/form.html'
    form_class = OffreForm
    success_url = reverse_lazy('offre:offre_list')

class OffreUpdateView(UpdateView):
    model = Offre
    template_name = 'offre/form.html'
    form_class = OffreForm
    success_url = reverse_lazy('offre:offre_list')
