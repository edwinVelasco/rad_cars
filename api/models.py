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
        db_table = "providers"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["code"]

    def __str__(self):
        return self.name


class Quotation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    price = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "quotations"
        ordering = ["price"]

    def __str__(self):
        return f'{self.product} {self.price}'

