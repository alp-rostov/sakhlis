from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import RepairerList, OrderList
from .filters import RepFilter, OrderFilter
from .forms import RepairerForm, BaseRegisterForm, OrderForm, OrderFormUpdate


class RepairerL(ListView):
    model = RepairerList
    context_object_name = 'repairer'
    template_name = 'repairer_list.html'
    queryset = RepairerList.objects.all().order_by('s_name').values('s_name', 'city', 'name',
                                                                    'phone', 'email', 'foto', 'pk')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RepFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class RepaierD(DetailView):
    model = RepairerList
    template_name = 'repaier_detail.html'
    context_object_name = 'rep'


class RepaierCreate(LoginRequiredMixin, CreateView):
    model = RepairerList
    template_name = 'repaier_create.html'
    form_class = RepairerForm


class RepaierUpdate(UpdateView):
    model = RepairerList
    template_name = 'repaier_create.html'
    form_class = RepairerForm


class RepaierDelete(DeleteView):
    model = RepairerList
    template_name = 'repaier_delete.html'
    success_url = '/app'

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class NewOrder(CreateView):
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = '/app'

class OrderManagementSystem(ListView):
    model = OrderList
    context_object_name = 'order'
    template_name = 'order_list.html'
    ordering = ['-time_in']
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = OrderFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class OrderDatail(DetailView):
    model = OrderList
    template_name = 'order_detail.html'
    context_object_name = 'order'

class OrderUpdate(UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderFormUpdate
    success_url = '/app/list_order'

class OrderDelete(DeleteView):
    model = OrderList
    template_name = 'order_delete.html'
    success_url = '/app/list_order'




