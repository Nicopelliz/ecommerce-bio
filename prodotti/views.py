from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class ProductList(ListView):
    queryset = Product.objects.all()
    template_name = 'mercato.html'
    context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product
    template_name = 'dettaglio_prodotto.html'
    context_object_name = 'product'
