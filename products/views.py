class ProductView(View):
    @signin_check_decorator
    def get(self, request, product_id):
        try:
            product          = Product.objects.select_related("category").prefetch_related("themes", "material_set", "..").get(id=product_id)
            theme_ids        = list(product.themes.values_list("id", flat=True))
            related_products = Product.objects.filter(themes__id__in=theme_ids)
            is_liked         = Like.objects.filter(user=request.user, product_id=product_id).exists()
            
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
                    "id"           : product.id,
                    "name"         : product.name,
                    "price"        : product.price,
                    "image_urls"   : [image.url for image in product.productimage_set.all()]
                }for product in related_products]
            }

            return JsonResponse({'result':result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)
