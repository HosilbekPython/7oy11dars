from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category , Product , ProduktImage , Comment , Promotion , Filter

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk' , 'name')
    list_display_links = ('name',)
    prepopulated_fields = {"slug":("name",)}


class ProduktImageInline(admin.TabularInline):
    model = ProduktImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'slug' , 'descriotion' , 'price' , 'discount' , 'quantitiy' , 'volume' , 'category' , 'get_image')
    list_display_links = ('name',)
    prepopulated_fields = {"slug":("name",)}
    inlines = [ProduktImageInline]
    list_filter = ("category",)

    def get_image(self, product):
        image = product.product_images.all()
        if image.exists():
            return mark_safe(
                f'<img src="{image[0].image.url}" width="100" height="100" style="object-fit:cover; border-radius:5px;" />')
        return "No Image"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter faqat tegishli kategoriyadan chiqadi"""
        if db_field.name == "filters":
            if "category" in request.resolver_match.kwargs:
                category_id = request.resolver_match.kwargs["category"]
                category = Category.objects.get(id=category_id)

                # Tegishli filterlarni olish (asosiy va subkategoriya filterlari)
                valid_categories = category.get_descendants()
                valid_categories.append(category)
                kwargs["queryset"] = Filter.objects.filter(category__in=valid_categories)
            else:
                kwargs["queryset"] = Filter.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


    get_image.short_description = "Image"



admin.site.register(ProduktImage)


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug' , 'category')
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("category",)


admin.site.register(Comment)
admin.site.register(Promotion)
