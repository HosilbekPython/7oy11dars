from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import JsonResponse

from .models import Category, Product, ProduktImage, Comment, Promotion, Filter

# ProductForm ni yaratamiz
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Asosiy kategoriya tanlanganda, subkategoriyalarni ko'rsatish
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Category.objects.filter(parent_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()

        # Subkategoriya tanlanganda, filterlarni ko'rsatish
        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                subcategory = Category.objects.get(id=subcategory_id)
                valid_categories = subcategory.get_descendants(include_self=True)
                self.fields['filters'].queryset = Filter.objects.filter(category__in=valid_categories)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.subcategory:
            self.fields['filters'].queryset = Filter.objects.filter(category=self.instance.subcategory)


# CategoryAdmin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        # Faqat asosiy kategoriyalarni ko'rsatish
        return super().get_queryset(request).filter(parent=None)


# ProduktImageInline
class ProduktImageInline(admin.TabularInline):
    model = ProduktImage
    extra = 0


# ProductAdmin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm  # ProductForm ni shu yerda ishlatamiz
    list_display = ('name', 'slug', 'descriotion', 'price', 'discount', 'quantitiy', 'volume', 'category', 'get_image')
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProduktImageInline]
    list_filter = ("category",)

    def get_image(self, product):
        image = product.product_images.all()
        if image.exists():
            return mark_safe(
                f'<img src="{image[0].image.url}" width="100" height="100" style="object-fit:cover; border-radius:5px;" />')
        return "No Image"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Faqat asosiy kategoriyalarni ko'rsatish
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    get_image.short_description = "Image"

    class Media:
        js = ('admin/js/product_admin.js',)  # JavaScript faylini ulash

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-subcategories/', self.admin_site.admin_view(self.get_subcategories), name='get_subcategories'),
            path('get-filters/', self.admin_site.admin_view(self.get_filters), name='get_filters'),
        ]
        return custom_urls + urls

    def get_subcategories(self, request):
        category_id = request.GET.get('category_id')
        if category_id:
            subcategories = Category.objects.filter(parent_id=category_id).values('id', 'name')
            return JsonResponse(list(subcategories), safe=False)
        return JsonResponse([], safe=False)

    def get_filters(self, request):
        category_id = request.GET.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            valid_categories = category.get_descendants(include_self=True)
            filters = Filter.objects.filter(category__in=valid_categories).values('id', 'name')
            return JsonResponse(list(filters), safe=False)
        return JsonResponse([], safe=False)


# FilterAdmin
@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("category",)


# Comment va Promotion modellarini ro'yxatdan o'tkazamiz
admin.site.register(Comment)
admin.site.register(Promotion)