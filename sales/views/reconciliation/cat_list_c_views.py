from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from sales.forms import CatListCForm
from sales.models import CatListC


# CatListC CRUD
class CatListCView(ListView):
    model = CatListC
    template_name = 'reconciliation/cat_list_c/cat_list_c.html'
    context_object_name = 'items'

class CatListCCreateView(CreateView):
    model = CatListC
    form_class = CatListCForm
    template_name = 'reconciliation/cat_list_c/cat_list_c_form.html'
    success_url = reverse_lazy('catlistc_list')

class CatListCUpdateView(UpdateView):
    model = CatListC
    form_class = CatListCForm
    template_name = 'reconciliation/cat_list_c/cat_list_c_form.html'
    success_url = reverse_lazy('catlistc_list')


class CatListCDeleteView(DeleteView):
    model = CatListC
    success_url = reverse_lazy('catlistc_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)