import json

from django.http        import JsonResponse
from django.views       import View

from products.models    import Category, Product, ThemeProduct, Theme, Material, ProductImage, ProductOption, Size, Color, ProductSet
from users.models       import Like
# from core.utils         import SigninCheckDecorator

class SetProductDetailView(View):
    # @SigninCheckDecorator
    def get(self, request, product_id):
        try:
            product        = Product.objects.get(id=product_id)
            product_images     = product.productimage_set.all()
            image_objects      = [x for x in product_images]
            sub_products = ProductSet.objects.filter(product_set=product)
            # like_bool          = Like.objects.filter(user=request.user).exists()

            inclueded_product  = [x for x in sub_products]
            
            
            result_list = [
                {
                    "id"               : product.id,
                    "name"             : product.name,
                    "price"            : product.price,
                    "information"      : product.information,
                    "keyword"          : product.keyword,
                    # "users_like"       : like_bool,
                    "detail_image"     : [{
                        "url"          : image.url,
                        "alt"          : image.alt
                    }for image in image_objects],
                }
            ]

            return JsonResponse({'result':result_list}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)