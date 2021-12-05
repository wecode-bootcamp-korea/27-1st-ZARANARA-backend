import json

from django.views   import View
from django.http    import JsonResponse

from .models        import Category, Product, ProductOption, ProductSet, Theme, ThemeProduct

class ProductMainView(View): 
    def get(self, request): 
        slide_item = []
        items   = ThemeProduct.objects.select_related('product','theme').filter(theme = Theme.objects.get(id =3))[:3]
        slide_item = [{'slide_id':item.product.id,'slide_image' : item.product.productimage_set.all()[0].url} for item in items]

        list_item = []
        items = Product.objects.select_related('category')\
                                    .filter(category__name='선물아이디어').order_by('-price')[:2]
        for item in items: 
            product_items = ProductSet.objects.filter(product_set = item)
            list_item.append(
                {
                    'set_image'    : item.productimage_set.all()[0].url,
                    'set_item': [
                        {
                            'id'        : product_item.product.id,
                            'name'      : product_item.product.name,
                            'keyword'   : product_item.product.keyword,
                            'price'     : product_item.product.price,
                            'x_position': product_item.x_position,
                            'y_position': product_item.y_position
                    } 
                    for product_item in product_items
                    ]
                }
            )
        return JsonResponse({'slide_item': slide_item, 'list_item': list_item}, status = 200)

