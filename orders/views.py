import json

from django.http.response   import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View

from products.models        import Product, ProductImage, ProductOption 
#                         (이름, 가격, 제품번호id?), (알트값, 유알엘), (사이즈)
from users.models           import User, Cart
from zara.settings          import SECRET_KEY, ALGORITHM
from core.utils             import SigninDecorator


class UserCartView(View):
    @SigninDecorator
    def post(self, request):
        try:
            #유저 정보가 맞으면,
            data = json.loads(request.body)
            user = request.user
            product = Product.objects.get(id=data['id'])
            product_option = product.productoption_set.all()
            size
            상품의 장바구니를 담아라(담고 있어야 하는 정보6가지)
            
            담은 장바구니를 한개의 이미지를 삭제한다면, 장바구니의 이미지만 삭제
            
            딤은 장바구니를 모두 삭제하기 버튼을 누른다면, 장바구니의 모두 삭제


            Cart.objects.create(
                {
                    user = user,
                    product_option = Cart.objects.productoption
                    # 상품이름 : 
                    # 가격 :
                    # 이미지유알에 : 
                    # 이미지알트값 :
                    # 제품번호 : 
                    # 사이즈 : 


                }

            )
            return JsonResponse({'' : ''}, status= 200)
        except:
            return JsonResponse({'' : ''}, status= 401)