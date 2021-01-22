from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Food


class ProductList(ListView):
    queryset = Food.objects.all()
    template_name = 'mercato.html'
    context_object_name = 'products'
