from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import RepairerList, CityDirectory
# from .filters import RepFilter
# from .forms import RepairerForm
class RepairerL(ListView):
    model = CityDirectory
    context_object_name = 'city'
    template_name = 'base.html'
    # paginate_by = 2
    # #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = RepFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['filterset'] = self.filterset
    #     context['get'] = 'wwwwwwwwwwwwwwwwwww'
    #     return context
    #

# Create your views here.

from django.shortcuts import render
# from cms.plugin_rendering import render_plugin

def my_view(request):
    my_data = CityDirectory.objects.all()
    # my_plugin = render_plugin(request, plugin_type='MyPluginType', context={'my_data': my_data})
    return render(request, 'base.html', {'my_plugin': 'wwwwww'})
