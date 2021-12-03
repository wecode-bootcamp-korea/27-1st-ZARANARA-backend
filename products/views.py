import json

from django.http            import JsonResponse
from django.views           import View

from products.models        import Category, Product, ThemeProduct, Theme, Material, ProductImage, ProductOption, Size, Color

class DetailView(View):
    def get(self, request, product_id):
        try:
            product_data           = Product.objects.get(id=product_id)
            product_materials_data = product_data.material_set.all()
            product_option_data    = product_data.productoption_set.all() 
            product_images_data    = product_data.productimage_set.all()
            
            product_theme = product_data.themeproduct_set.get(product=product_data.id)
            theme_products = ThemeProduct.objects.filter(theme=product_theme.id)

            material_objects   = [x for x in product_materials_data]
            image_objects      = [x for x in product_images_data]
            option_objects     = [x for x in product_option_data]
            theme_product_list = [x for x in theme_products]
            
            product_name        = product_data.name
            product_price       = product_data.price
            product_id          = product_data.id
            product_information = product_data.information
            product_keyword     = product_data.keyword
            product_category    = product_data.category.name

            result_list = [
                {
                    "id"             : product_id,
                    "name"           : product_name,
                    "price"          : product_price,
                    "information"    : product_information,
                    "keyword"        : product_keyword,
                    "category"       : product_category,
                    "material"       : [{
                        "name"       : material.name,
                        "caution"    : material.caution 
                    }for material in material_objects],
                    "detail_image"   : [{
                        "url"        : image.url,
                        "alt"        : image.alt
                    }for image in image_objects],
                    "product_option" : [{
                        "size"       : option.size.name,
                        "color"      : option.color.name,
                        "stock"      : option.stock
                    }for option in option_objects],
                    "theme_products" : [{
                        "id"         : theme_product.product.id,
                        "name"       : theme_product.product.name,
                        "price"      : theme_product.product.price,
                        "image_url"  : [x.url for x in theme_product.product.productimage_set.all()]
                    }for theme_product in theme_product_list]
                }
            ]

            return JsonResponse({'result':result_list}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)

