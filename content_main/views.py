from lib2to3.fixes.fix_input import context
from msilib.schema import ListView

from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Category , Product


# Create your views here.

class HomePageCategoryAndProduct(ListView):
    queryset = Product.objects.all()[:6]
    context_object_name = "products"
    template_name = 'index.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories']= Category.objects.filter(parent = None)
        return context


class CategoryFilterView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'index.html'
    def get_queryset(self):
        category_slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(category = category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories']= Category.objects.filter(parent = None)
        return context