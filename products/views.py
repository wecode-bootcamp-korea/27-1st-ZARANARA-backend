import json

from django.http        import JsonResponse
from django.views       import View

from products.models    import Category, Product, ThemeProduct, Theme, Material, ProductImage, ProductOption, Size, Color
from users.models       import Like, User
from core.utils         import SigninCheckDecorator

class ProductDetailView(View):
    @SigninCheckDecorator
    def get(self, request, product_id):
        try:
            product            = Product.objects.get(id=product_id)
            product_materials  = product.material_set.all()
            product_option     = product.productoption_set.all() 
            product_images     = product.productimage_set.all()
            user               = request.GET.get("user",0)
            like_bool          = Like.objects.filter(user=user).exists() #임시로 유저아이디 1번을 지정하였음. 추후 토큰 데코레이터 추가 예정

            product_theme  = product.themeproduct_set.get(product=product.id)
            theme_products = ThemeProduct.objects.filter(theme=product_theme.id)

            material_objects   = [x for x in product_materials]
            image_objects      = [x for x in product_images]
            option_objects     = [x for x in product_option]
            theme_product_list = [x for x in theme_products]
            
            result_list = [
                {
                    "id"               : product.id,
                    "name"             : product.name,
                    "price"            : product.price,
                    "information"      : product.information,
                    "keyword"          : product.keyword,
                    "category"         : product.category.name,
                    "users_like"       : like_bool,
                    "material_name"    : [material.name for material in material_objects],
                    "material_caution" : [material.caution for material in material_objects],
                    "detail_image"     : [{

                        "url"          : image.url,
                        "alt"          : image.alt
                    }for image in image_objects],
                    "product_option"   : [{
                        "size"         : option.size.name,
                        "color"        : option.color.name,
                        "stock"        : option.stock
                    }for option in option_objects],
                    "theme_products"   : [{
                        "id"           : theme_product.product.id,
                        "name"         : theme_product.product.name,
                        "price"        : theme_product.product.price,
                        "image_url"    : [x.url for x in theme_product.product.productimage_set.all()]
                    }for theme_product in theme_product_list]
                }
            ]

            return JsonResponse({'result':result_list}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)


            
