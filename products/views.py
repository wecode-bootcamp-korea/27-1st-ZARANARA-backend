import json

from django.views   import View
from django.http    import JsonResponse

from .models        import Theme, ThemeProduct, Product, ProductSet, Category

class ProductThemeView(View): 
    def get(self, request): 
        slide_item = []
        offset     = int(request.GET.get('offset', 0))
        limit      = int(request.GET.get('limit', 3))
        items      = ThemeProduct.objects.select_related('product','theme')\
                            .filter(theme = Theme.objects.get(name='크리스마스'))[offset:limit]

        slide_item = [
            {
                'slide_id'   : item.product.id,
                'slide_image': item.product.productimage_set.all()[0].url,
                'alt'        : item.product.productimage_set.all()[0].alt
            } for item in items
            ]

        return JsonResponse({'slide_item': slide_item}, status = 200)

class ProductSetListView(View):
    def get(self, request):
        list_item = []
        offset    = int(request.GET.get('offset', 0))
        limit     = int(request.GET.get('limit', 2))
        order     = request.GET.get('order', '-price')
        items     = Product.objects.select_related('category')\
                                    .filter(category__name='선물아이디어').order_by(order)[offset:limit]

        for item in items: 
            product_items = ProductSet.objects.filter(product_set = item)
            list_item.append(
                {
                    'set_id'   : item.id,
                    'set_image': item.productimage_set.all()[0].url,
                    'set_alt'  : item.productimage_set.all()[0].alt,
                    'set_item' : [
                        {
                            'id'        : product_item.product.id,
                            'name'      : product_item.product.name,
                            'keyword'   : product_item.product.keyword,
                            'price'     : product_item.product.price,
                            'x_position': product_item.x_position,
                            'y_position': product_item.y_position,
                            'item_alt'  : product_item.product.productimage_set.all()[0].alt
                    } 
                    for product_item in product_items
                    ]
                }
            )
        return JsonResponse({'list_item': list_item}, status = 200)

class ProductListView(View):
    def get(self, request, category_id):
        category = Category.objects.get(id = category_id)
        order    = str(request.GET.get('order','created_at'))
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 4))
        items    = Product.objects.select_related('category').filter(category = category).order_by(order)[offset:limit]
        results  = [
            {
                'id'   : item.id,
                'name' : item.name,
                'price': item.price,
                'image': item.productimage_set.all()[0].url
            }
            for item in items
            ]
        return JsonResponse({'results' : results, 'count': len(items)}, status =200)