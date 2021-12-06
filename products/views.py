import json

from django.views   import View
from django.http    import JsonResponse

from .models        import Theme, ThemeProduct

class ProductSlideView(View): 
    def get(self, request): 
        slide_item = []
        offset     = int(request.GET.get('offset', 0))
        limit      = int(request.GET.get('limit', 3))
        items      = ThemeProduct.objects.select_related('product','theme').filter(theme = Theme.objects.get(id =3))[offset:limit]

        slide_item = [{'slide_id':item.product.id,'slide_image' : item.product.productimage_set.all()[0].url, 'alt' : item.product.productimage_set.all()[0].alt} for item in items]

        return JsonResponse({'slide_item': slide_item}, status = 200)