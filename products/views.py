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
            product_images = product.productimage_set.all()
            image_objects  = [x for x in product_images]
            sub_products   = ProductSet.objects.filter(product_set_id=product)
            # like_bool    = Like.objects.filter(user=request.user).exists()

            sub_product_list = [x.product for x in sub_products]
            
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
                    "sub_products"     : [{
                        "id"           : sub_product.id,
                        "name"         : sub_product.name,
                        "price"        : sub_product.price,
                        "size"         : sub_product.productoption_set.all()[0].size.name,
                        "color"        : sub_product.productoption_set.all()[0].color.name,
                        "sub_product_image" : [{
                            "url"      : sub_product_image.url,
                            "alt"      : sub_product_image.alt
                        }for sub_product_image in sub_product.productimage_set.all()]
                    }for sub_product in sub_product_list]
                }
            ]

            return JsonResponse({'result':result_list}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)



# class LikeToggleView(View):
    # def get(self, request, product_id):
        #토큰을 받아 유저 아이디를 확인한다.
        #유저가 좋아요 버튼을 누른 상품의 아이디를 가져온다.
        #like 테이블에 유저 아이디와 상품 아이디가 일치하는 데이터가 있는지 확인한다.
        #있다면 해당 데이터를 삭제한다.
        #없다면 해당 데이터를 추가한다.
        #트렌젝션을 이용하여 상세페이지에 바로 반영되도록 한다.
        