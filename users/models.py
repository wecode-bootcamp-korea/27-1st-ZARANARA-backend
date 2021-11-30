from django.db       import models

from core.models     import TimeStampModel
from products.models import Product
from stocks.models   import Stock

class User(TimeStampModel): 
    name     = models.CharField(max_length=300)
    email    = models.CharField(max_length=300, unique = True)
    password = models.BinaryField(max_length=300)
    phone    = models.CharField(max_length=100, null = True)
    cash     = models.DecimalField(default=0, max_digits=65, decimal_places=2)
    
    class Meta: 
        db_table = 'users'

class Address(models.Model): 
    name    = models.CharField(max_length=300, null = True)
    zipcode = models.CharField(max_length=300, null = True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'address'

class Cart(models.Model): 
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    stock    = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta: 
        db_table = 'carts'

class Like(models.Model): 
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'likes'