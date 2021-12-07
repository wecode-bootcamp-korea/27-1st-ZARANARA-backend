from django.shortcuts import render

from django.views   import View
from django.http    import JsonResponse

from .models        import Theme, ThemeProduct, Product, ProductSet, Category

class ProductSetListView(View):
    def get(self, request):
        list_item = []
        offset    = int(request.GET.get('offset', 0))
        limit     = int(request.GET.get('limit', 2))
        order     = request.GET.get('order', '-price')
        items     = Product.objects.select_related('category').filter(category__name='선물아이디어').order_by(order)[offset:limit]
        # 하드 코딩은 절대 No!!

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

    def get(self, request, category_id):
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 100)) if limit > 100: return JsonResponse("ERROR")
        theme_id    = int(request.GET.get("themeId", None)
        category_id = int(request.GET.get("categoryId", None)
        ordering    = str(request.GET.get('ordering','created_at'))

        q = Q()

        if theme_id:
            q &= Q(themes__id = theme_id)

        if category_id:
            q &= Q(category_id = category_id)

        products    = Product.objects.filter(q).order_by(ordering)
        total_count = products.count()
        results     = [{
            'id'   : product.id,
            'name' : product.name,
            'price': product.price,
            'image': product.productimage_set.all()[0].url,
            'alt'  : product.productimage_set.all()[0].alt
        } for product in products[offset:limit]]

        return JsonResponse({'results' : results, 'total_count': total_count}, status =200)
