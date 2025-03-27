from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from sales.forms import SlicerListForm
from sales.models import SlicerList

# SlicerList CRUD
class SlicerListView(ListView):
    model = SlicerList
    template_name = 'reconciliation/slicer_list/slicer_list.html'
    context_object_name = 'items'

class SlicerCreateView(CreateView):
    model = SlicerList
    form_class = SlicerListForm
    template_name = 'reconciliation/slicer_list/slicer_list_form.html'
    success_url = reverse_lazy('slicer_list')

class SlicerUpdateView(UpdateView):
    model = SlicerList
    form_class = SlicerListForm
    template_name = 'reconciliation/slicer_list/slicer_list_form.html'
    success_url = reverse_lazy('slicer_list')

# class SlicerDeleteView(DeleteView):
#     model = SlicerList
#     template_name = 'crud/slicer_confirm_delete.html'
#     success_url = reverse_lazy('slicer_list')

class SlicerDeleteView(DeleteView):
    model = SlicerList
    success_url = reverse_lazy('slicer_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)