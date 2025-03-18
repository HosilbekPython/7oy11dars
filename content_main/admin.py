from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category , Product , ProduktImage , Comment , Promotion

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

    def get_image(self, product):
        image = product.product_images.all()
        if image.exists():
            return mark_safe(
                f'<img src="{image[0].image.url}" width="100" height="100" style="object-fit:cover; border-radius:5px;" />')
        return "No Image"

    get_image.short_description = "Image"


admin.site.register(ProduktImage)
admin.site.register(Comment)
admin.site.register(Promotion)
