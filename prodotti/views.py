from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class ProductList(ListView):
    queryset = Product.objects.all()
    template_name = 'mercato.html'
    context_object_name = 'products'
