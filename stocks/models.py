from django.db       import models

from core.models     import TimeStampModel
from products.models import Product


class Stock(TimeStampModel): 
    price    = models.DecimalField(default=0, max_digits=65, decimal_places=2)
    sales    = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    size     = models.ForeignKey('Size', on_delete=models.CASCADE)
    color    = models.ForeignKey('Color', on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'stocks'

class Size(models.Model): 
    name        = models.CharField(max_length=100)
    information = models.CharField(max_length=500)

    class Meta: 
        db_table = 'sizes'

class Color(models.Model): 
    name = models.CharField(max_length=100)

    class Meta: 
        db_table = 'colors'
