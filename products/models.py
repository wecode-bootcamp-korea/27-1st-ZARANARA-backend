from django.db   import models

from core.models import TimeStampModel

class Category(models.Model): 
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image_url   = models.URLField(max_length=2000)

    class Meta: 
        db_table = 'categories'

class Product(TimeStampModel): 
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(default=0, max_digits=65, decimal_places=2)
    information = models.CharField(max_length=500)
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'products'

class ThemeProduct(models.Model): 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    theme   = models.ForeignKey('Theme', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'theme_products'

class Theme(models.Model): 
    name = models.CharField(max_length=100)

    class Meta: 
        db_table = 'themes'

class Material(models.Model): 
    name    = models.CharField(max_length=100)
    caution = models.CharField(max_length=500)
    product = models.ManyToManyField('Product')

    class Meta: 
        db_table = 'materials'

class ProductImage(models.Model): 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    alt     = models.CharField(max_length=200)
    url     = models.URLField(max_length=2000)

    class Meta: 
        db_table = 'product_images'

class ProductOption(TimeStampModel): 
    sales               = models.IntegerField(default=0)
    stock               = models.IntegerField(default=0)
    thumbnail_image_url = models.URLField(max_length=2000)
    size                = models.ForeignKey('Size', on_delete=models.CASCADE)
    color               = models.ForeignKey('Color', on_delete=models.CASCADE)
    product             = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'product_options'

class Size(models.Model): 
    name        = models.CharField(max_length=100)
    information = models.CharField(max_length=500)

    class Meta: 
        db_table = 'sizes'

class Color(models.Model): 
    name = models.CharField(max_length=100)

    class Meta: 
        db_table = 'colors'
