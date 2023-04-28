from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import RepairerList
from .filters import RepFilter
from .forms import RepairerForm


# Create your views here.
class RepairerL(ListView):
    model = RepairerList
    context_object_name = 'repairer'
    template_name = 'repairerlist.html'
    queryset = RepairerList.objects.all().order_by('s_name').values('s_name', 'city', 'name',
                                                                    'phone', 'email', 'foto', 'pk')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RepFilter(self.request.GET, queryset)
        # print(self.filterset.queryset[1].rating_sum)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class RepaierD(DetailView):
    model = RepairerList
    template_name = 'repaierdar.html'
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


def home(request):
    return render(request, 'index.html')
