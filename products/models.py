from django.db   import models

from core.models import TimeStampModel

class Category(models.Model): 
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image_url   = models.URLField(max_length=2000)

    class Meta: 
        db_table = 'categories'

class ThemeProduct(models.Model): 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    theme   = models.ForeignKey('Theme', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'theme_products'


class Product(TimeStampModel): 
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(default=0, max_digits=65, decimal_places=2)
    information = models.CharField(max_length=500)
    keyword     = models.CharField(max_length=100, null=True)
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    themes      = models.ManyToManyField('Theme', through=ThemeProduct)
    
    class Meta: 
        db_table = 'products'

class ProductSet(models.Model): 
    product_set = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_set')
    product     = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_item')
    x_position  = models.IntegerField()
    y_position  = models.IntegerField()

    class Meta: 
        db_table = 'product_sets'

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
    size                = models.ForeignKey('Size', on_delete=models.CASCADE, null=True)
    color               = models.ForeignKey('Color', on_delete=models.CASCADE, null=True)
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
