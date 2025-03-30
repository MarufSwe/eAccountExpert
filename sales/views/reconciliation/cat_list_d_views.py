from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from sales.forms import CatListDForm
from sales.models import CatListD
from django.contrib.auth.mixins import LoginRequiredMixin


# CatListD CRUD
class CatListDView(LoginRequiredMixin, ListView):
    model = CatListD
    template_name = 'reconciliation/cat_list_d/cat_list_d.html'
    context_object_name = 'items'

class CatListDCreateView(CreateView):
    model = CatListD
    form_class = CatListDForm
    template_name = 'reconciliation/cat_list_d/cat_list_d_form.html'
    success_url = reverse_lazy('catlistd_list')

class CatListDUpdateView(UpdateView):
    model = CatListD
    form_class = CatListDForm
    template_name = 'reconciliation/cat_list_d/cat_list_d_form.html'
    success_url = reverse_lazy('catlistd_list')

class CatListDDeleteView(DeleteView):
    model = CatListD
    success_url = reverse_lazy('catlistd_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)