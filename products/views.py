import json
from django.core.exceptions import ValidationError

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import Product, ProductSet

class ProductSetListView(View):
    def get(self, request):
        list_item   = []
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 100))
        category_id = int(request.GET.get('categoryId',8))
        order       = request.GET.get('order', '-price')
        items       = Product.objects.select_related('category')\
                                    .filter(category=category_id).order_by(order)[offset:limit]
        
        if limit > 100:
            return JsonResponse({'MESSAGE':'LIMIT_ERROR'}, status = 400)

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
    # :8000/products?offset=0&limit=100&themeId = 1 (O)
    # :8000/products?offset=0&limit=100&categoryId = 100 (O)
    # :8000/products/category/10 (X)
    # :8000/categories/10/products(O)
    def get(self, request):
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 100))
        theme_id    = int(request.GET.get("themeId", None)) if request.GET.get("themeId", None) != None else None
        category_id = int(request.GET.get("categoryId", None)) if request.GET.get("categoryId", None) != None else None
        ordering    = str(request.GET.get('ordering','created_at'))

        q = Q()

        if limit > 100:
            return JsonResponse({'MESSAGE':'LIMIT_ERROR'}, status = 400)

        if theme_id:
            q &= Q(themes = theme_id)

        if category_id:
            q &= Q(category__id = category_id)

        products    = Product.objects.select_related('category').prefetch_related('productimage_set','themes').filter(q).order_by(ordering)
        total_count = products.count()
        results     = [{
            'id'   : product.id,
            'name' : product.name,
            'price': product.price,
            'image': product.productimage_set.all()[0].url,
            'alt'  : product.productimage_set.all()[0].alt
        } for product in products[offset:limit]]

        return JsonResponse({'results' : results, 'total_count': total_count}, status =200)