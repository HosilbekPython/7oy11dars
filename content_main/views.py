from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView , DetailView , CreateView, UpdateView , DeleteView

from .models import Category , Product , Comment
from .forms import CommentForms
from django.urls import reverse_lazy



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


class ProductDetaliViews(DetailView):
    model = Product
    context_object_name = "one_produk"
    pk_url_kwarg = "product_id"
    template_name = "shop-single_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = self.object

        category = product.category
        context['form_comment'] = CommentForms()
        context['products'] = Product.objects.filter(category=category)
        context['categories']= Category.objects.filter(parent = None)
        context['comment_fil'] = Comment.objects.filter(product = product)

        return context

class CommentSaveViews(CreateView):
    model = Comment
    form_class = CommentForms
    def get_success_url(self):
        product_id = self.kwargs.get("product_id")
        return reverse_lazy("product_detail" , kwargs = {"product_id" : product_id})

    def form_valid(self, form):
        form.instance.product = Product.objects.get(id=self.kwargs.get("product_id"))
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteCommentView(DeleteView):
    model = Comment
    pk_url_kwarg = "comment_id"
    template_name = "car_confirm_delete.html"

    def get_success_url(self):
        product_id = self.kwargs.get("product_id")
        return reverse_lazy("product_detail", kwargs={"product_id": product_id})

    def get_object(self, queryset=None):
        object = self.model.objects.get(id = self.kwargs.get("product_id"))
        return object

