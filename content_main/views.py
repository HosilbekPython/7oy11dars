from lib2to3.fixes.fix_input import context

from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView , DetailView , CreateView, UpdateView , DeleteView
from unicodedata import category

from .models import Category , Product , Comment , Promotion
from .forms import CommentForms
from django.urls import reverse_lazy
from django.views.generic import ListView



# Create your views here.

class HomePageCategoryAndProduct(ListView):
    queryset = Product.objects.all().order_by('-discount')[:6]
    context_object_name = "products_order_by_prosent"
    template_name = 'index.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories']= Category.objects.filter(parent = None)
        context['promotiones']= Promotion.objects.all()
        return context


class ShopingView(ListView):
    queryset = Product.objects.all().order_by('-discount')
    context_object_name = "productes"
    template_name = 'shop.html'

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")

        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                return Product.objects.filter(category__in=category.get_descendants()).order_by('-discount')

        return Product.objects.all().order_by('-discount')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category_slug = self.kwargs.get("category_slug")

        context['categories'] = Category.objects.filter(parent=None)
        context['selected_category'] = None
        context['subcategories'] = None

        if category_slug:
            selected_category = Category.objects.filter(slug=category_slug).first()
            context['selected_category'] = selected_category

            if selected_category:
                # Agar bu subkategoriya bo'lsa, uning parent kategoriya sini olish
                if selected_category.parent:
                    context['subcategories'] = Category.objects.filter(parent=selected_category.parent)
                else:
                    context['subcategories'] = Category.objects.filter(parent=selected_category)

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

