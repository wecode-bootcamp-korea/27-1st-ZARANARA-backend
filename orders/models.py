from django.db       import models

from core.models     import TimeStampModel
from products.models import ProductOption
from users.models    import User

class OrderStatus(models.Model): 
    name = models.CharField(max_length=200)

    class Meta: 
        db_table = 'order_status'

class Order(TimeStampModel): 
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'orders'

class OrderProduct(models.Model): 
    count           = models.IntegerField(default=1)
    tracking_number = models.CharField(max_length=500)
    stock           = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    order           = models.ForeignKey('Order', on_delete=models.CASCADE)
    delivery_status = models.ForeignKey('DeliveryStatus', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'order_products'

class DeliveryStatus(models.Model): 
    name = models.CharField(max_length=200)
    
    class Meta: 
        db_table = 'delivery_status'