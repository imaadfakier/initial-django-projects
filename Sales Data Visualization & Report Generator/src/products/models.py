from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(help_text='in GBP pounds £')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f"{self.name}-{self.created_on.strftime('%d/%m/%y')}"
        # return f"{self.name}"
        # return f"{self.name}-{self.created_on}"
        return f"{self.name}-{self.created_on.strftime('%d/%m/%y')}"
