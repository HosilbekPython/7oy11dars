from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    slug = models.SlugField(max_length=100 , unique=True)
    image = models.ImageField(upload_to="category/image/" , null=True , blank=True)
    parent = models.ForeignKey('self' , on_delete=models.SET_NULL , null=True , blank=True)

    def __str__(self):
        if not self.parent:
            return self.name
        return f"{self.parent.name} : {self.name}"

VOLUMES = {
    "kg":"Kilogram",
    "l": "Liter",
    "dona": "Dona"
}

class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250 , unique=True)
    descriotion = models.CharField(max_length=500 , null=True , blank=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    discount = models.IntegerField(default=0)
    quantitiy = models.IntegerField(default=50)
    volume = models.CharField(max_length=4 , choices=VOLUMES)
    category = models.ForeignKey(Category , on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ProduktImage(models.Model):
    image = models.ImageField(upload_to="product/images/")
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='product_images')

    def __str__(self):
        return self.product.name


class Comment(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='comment')
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}"
