from django.db import models


# Create your models here.

class Provider(models.Model):
    nit = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rad_cars_providers"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Mark(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = "rad_cars_marks"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=40)
    mark = models.ForeignKey(Mark, on_delete=models.PROTECT,
                             related_name='mark_models')

    class Meta:
        db_table = "rad_cars_models"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = "rad_cars_categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    stock = models.IntegerField(default=None, null=True, blank=True)
    mark_model = models.ForeignKey(Model, on_delete=models.PROTECT,
                                   null=True, default=None,
                                   related_name='marks_products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='categories')

    images = models.JSONField(blank=True, default=None, null=True)
    profit = models.IntegerField(blank=True, default=None)

    transmission = models.CharField(max_length=50, null=True, blank=True,
                                    default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rad_cars_products"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_net_price(self):
        if self.price and self.profit:
            return self.price*(self.profit/100) + self.price
        return 0

    net_price = property(get_net_price)


class Quotation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    price = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rad_cars_quotations"
        ordering = ["price"]

    def __str__(self):
        return f'{self.product} {self.price}'

