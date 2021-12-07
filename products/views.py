import json

from django.http        import JsonResponse
from django.views       import View

from products.models    import Category, Product, ThemeProduct, Theme, Material, ProductImage, ProductOption, Size, Color, ProductSet
from users.models       import Like, User
from core.utils         import signin_check_decorator

class ProductView(View):
    @signin_check_decorator
    def get(self, request, product_id):
        try:
            product          = Product.objects.get(id=product_id)
            theme_ids        = list(product.themes.values_list("id", flat=True))
            related_products = Product.objects.filter(themes__id__in=theme_ids)
            is_liked         = Like.objects.filter(user=request.user, product=product_id).exists()
            
            result = {
                "id"                : product.id,
                "name"              : product.name,
                "price"             : product.price,
                "information"       : product.information,
                "keyword"           : product.keyword,
                "category"          : product.category.name,
                "is_liked"          : is_liked,
                "material_names"    : [material.name for material in product.material_set.all()],
                "material_cautions" : [material.caution for material in product.material_set.all()],
                "images"            : [{"url" : image.url, "alt" : image.alt } for image in product.productimage_set.all()],
                "product_options"   : [{
                    "size"          : option.size.name,
                    "color"         : option.color.name,
                    "stock"         : option.stock
                } for option in product.productoption_set.all()],
                "related_products"  : [{
                    "id"            : product.id,
                    "name"          : product.name,
                    "price"         : product.price,
                    "image_urls"    : [image.url for image in product.productimage_set.all()]
                }for product in related_products]
            }

            return JsonResponse({'result':result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)

class SetProductView(View):
    @signin_check_decorator
    def get(self, request, product_id):
        try:
            product        = Product.objects.get(id=product_id)
            is_liked       = Like.objects.filter(user=request.user, product=product_id).exists()
            
            result = {
                "id"           : product.id,
                "name"         : product.name,
                "price"        : product.price,
                "information"  : product.information,
                "keyword"      : product.keyword,
                "category"     : product.category.name,
                "is_liked"     : is_liked,
                "images"       : [{"url" : image.url, "alt" : image.alt} for image in product.productimage_set.all()],
                "sub_products" : [{
                    "id"       : product.id,
                    "name"     : product.name,
                    "price"    : product.price,
                    "size"     : product.productoption_set.all()[0].size.name,
                    "color"    : product.productoption_set.all()[0].color.name,
                    "images" : [{
                        "url"   : image.url,
                        "alt"   : image.alt
                    }for image in product.productimage_set.all()]
                } for product.product in ProductSet.objects.filter(product_set_id=product)]
            }

            return JsonResponse({'result':result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)
