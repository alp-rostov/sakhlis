from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import RepairerList
from .filters import RepFilter
from .forms import RepairerForm


# Create your views here.
class RepairerL(ListView):
    model = RepairerList
    context_object_name = 'repairer'
    template_name = 'repairerlist.html'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RepFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # context['get'] = CityDirectory.objects.all()
        return context


class RepaierD(DetailView):
    model = RepairerList
    template_name = 'repaierdar.html'
    context_object_name = 'rep'


class RepaierCreate(CreateView):
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
    success_url = '/'
