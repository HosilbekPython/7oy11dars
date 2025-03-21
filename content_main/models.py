from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    slug = models.SlugField(max_length=100 , unique=True)
    image = models.ImageField(upload_to="category/image/" , null=True , blank=True)
    parent = models.ForeignKey('self' , on_delete=models.SET_NULL , null=True , blank=True)
    is_special = models.BooleanField(default=False)

    def __str__(self):
        if not self.parent:
            return self.name
        return f"{self.parent.name} : {self.name}"

    def get_descendants(self):
        categories = [self]
        subcategories = Category.objects.filter(parent=self)
        for subcat in subcategories:
            categories.extend(subcat.get_descendants())
        return categories


class Filter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100 , unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="filters"
    )

    def __str__(self):
        return self.name

    def clean(self):
        if not self.category.products.exists() and not Category.objects.filter(parent=self.category).exists():
            raise ValidationError("Filter faqat mahsulotga ega bo‘lgan kategoriyaga qo‘shilishi mumkin!")




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
    category = models.ForeignKey(Category , on_delete=models.PROTECT , related_name="products")
    filters = models.ManyToManyField(Filter , null=True , blank=True)

    def __str__(self):
        return self.name

    def get_image(self):
        images = self.images.all()
        if images:
            return images[0].image.url
        return "https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png?20210521171500"

    def get_price(self):
        if self.discount > 0:
            return self.price - self.price * self.discount / 100
        return self.price


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
    reyting = models.IntegerField(null=True , blank=True)

    def __str__(self):
        return f"{self.user.username}"


class Promotion(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=150)
    text = models.CharField(max_length=300)
    image = models.FileField(upload_to="promotion/image/" , null=True , blank=True , validators=[FileExtensionValidator(allowed_extensions=["png" , "jpg"])])

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL  , null=True)
    create = models.DateTimeField(auto_now_add=True)
    discontinued = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=15 , decimal_places=2)

    def __str__(self):
        return f"{self.user.usename} - {self.create}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.SET_NULL  , null=True)
    quantitiy = models.IntegerField()

    def __str__(self):
        return f"{self.product.name}"

class City(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class DeliverAddress(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=13)
    city = models.ForeignKey(City , on_delete=models.SET_NULL  , null=True)
    address = models.CharField(max_length=250)
    comment = models.CharField(max_length=1000 , null=True , blank=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.last_name}"










