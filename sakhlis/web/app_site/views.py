from django.views.generic import ListView, DetailView
from .models import City, Repairer
from .filters import CityFilter, RepFilter

# Create your views here.

class CityList(ListView):
    model = City
    ordering = 'name'
    template_name = 'citylist.html'
    context_object_name = 'city'


class City(DetailView):
    model = City
    template_name = 'city.html'
    context_object_name = 'city'




class RepairerList( ListView):
    model = Repairer
    context_object_name = 'repairer'
    template_name = 'repairerlist.html'
    paginate_by = 5
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RepFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # context['get'] = Repairer.objects.all()
        return context



class Repairer(DetailView):
    model = Repairer
    context_object_name = 'repairer'
    template_name = 'repairer.html'

    # Переопределяем функцию получения списка

