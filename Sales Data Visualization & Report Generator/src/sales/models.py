from django.db import models
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from .utils import generate_code
from django.shortcuts import reverse

# Create your models here.
class Position(models.Model):
    # pass
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created_on = models.DateTimeField(blank=True)

    def __str__(self):
        return f'ID: {self.id}, product: {self.product.name}, quantity: {self.quantity}'
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)
    
    def get_sales_id(self):
        # sale_obj = self.sale_set.first()
        # sale_obj = self.sale_set.all()
        sale_obj = self.sale_set.first() # <= how to perform a reverse relationship between classes
        return sale_obj.id
    
    def get_customer_name(self):
        sale_obj = self.sale_set.first()
        return sale_obj.customer.name

class Sale(models.Model):
    # pass
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Sales for the amount of £{self.total_price}'
    
    def save(self, *args, **kwargs):
        if self.transaction_id == '':
            self.transaction_id = generate_code()
        if self.created_on == None:
            self.created_on = timezone.now()
        return super().save(*args, **kwargs)
    
    def get_positions(self):
        return self.positions.all()
    
    def get_absolute_url(self):
        return reverse('sales:detail', kwargs={'pk':self.pk})

class CSV(models.Model):
    # pass
    csv_file = models.FileField(upload_to='csvs', null=True)
    filename = models.CharField(max_length=120, null=True)
    # activated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.filename)