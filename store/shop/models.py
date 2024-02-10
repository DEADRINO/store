from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique=True)
    image = models.ImageField(upload_to='image/category/', blank=True, null=True)

    class Meta:
        ordering = ['name',]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique=True)
    image = models.ImageField(upload_to='image/subcategory/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='image/products/images',
                              blank=True, null=True)
    thumbnail = models.ImageField(upload_to='image/products/thumbnails',
                                  blank=True, null=True)
    medium_size = models.ImageField(upload_to='image/products/medium_size',
                                    blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')


class CartItem(models.Model):
    objects = models.Manager()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    shop_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

