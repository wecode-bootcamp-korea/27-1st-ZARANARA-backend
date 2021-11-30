from django.db   import models

from core.models import TimeStampModel

class Product(TimeStampModel): 
    name        = models.CharField(max_length=100)
    information = models.CharField(max_length=500)
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'products'

class Category(models.Model): 
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image_url   = models.URLField(max_length=2000)

    class Meta: 
        db_table = 'categories'

class ThemePruduct(models.Model): 
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
    product = models.ManyToManyField(Product)

    class Meta: 
        db_table = 'materials'

class Image(models.Model): 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    alt     = models.CharField(max_length=200)
    url     = models.URLField(max_length=2000)

    class Meta: 
        db_table = 'images'
