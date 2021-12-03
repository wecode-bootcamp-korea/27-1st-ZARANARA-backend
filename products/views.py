import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from products.models        import Category, Product, ThemeProduct, Theme, Material, ProductImage, ProductOption, Size, Color

# enum class

class DetailView(View):
    def get(self, request, product_id):
        product_data = Product.objects.get(id=product_id)
        product_materials_data = product_data.material_set.all() #소재 케어
        product_option_data = product_data.productoption_set.all() 
        #옵션 - 사이즈, 컬러, 재고수량, 썸네일 이미지(옵션별), 판매수량


        product_name = product_data.name
        product_price = product_data.price
        product_id = product_data.id
        product_information = product_data.information
        product_keyword = product_data.keyword
        product_category = product_data.category.name

        material_objects = [x for x in product_materials_data]


        # 결과값 리스트 1 
        # material_caution = product_material_data.caution
        # print(f"확인중 {product_materials_data}")
        # print(f"확인중 {material_objects[0].name}")
        # result_list = [
        #     {
        #         "id" : product_id,
        #         "name" : product_name,
        #         "price" : product_price,
        #         "information" : product_information,
        #         "keyword" : product_keyword,
        #         "category" : product_category,
        #         "material_name" : [material.name for material in material_objects],
        #         "material_caution" : [material.caution for material in material_objects]
        #     }
        # ]



        # 소재정보를 가져오는 미리 가져와 리스트로 묶는 코드
        a = [material.name for material in material_objects]
        b = [material.caution for material in material_objects]
        m_list = []
        for i in zip(a,b):
            m_list.append(i)

        # 결과값 리스트 2
        result_list = [
            {
                "id" : product_id,
                "name" : product_name,
                "price" : product_price,
                "information" : product_information,
                "keyword" : product_keyword,
                "category" : product_category,
                "material" : m_list
            }
        ]

        return JsonResponse({'result':result_list}, status=200)
