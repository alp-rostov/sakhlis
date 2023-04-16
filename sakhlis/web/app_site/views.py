from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import City, Repairer
from .filters import CityFilter

from pprint import pprint
# Create your views here.

class CityList(ListView):
    model = City
    ordering = 'name'
    template_name = 'citylist.html'
    context_object_name = 'city'
    paginate_by = 2
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = CityFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        pprint(context)
        return context




class City(DetailView):
    model = City
    template_name = 'city.html'
    context_object_name = 'city'



class RepairerList(ListView):
    model = Repairer
    context_object_name = 'repairer'
    template_name = 'repairerlist.html'

class Repairer(DetailView):
    model = Repairer
    context_object_name = 'repairer'
    template_name = 'repairer.html'
