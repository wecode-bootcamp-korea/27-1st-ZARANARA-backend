import json

from django.http.response   import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View

from products.models        import Color, Product, ProductImage, ProductOption, Size 
#                         (이름, 가격, 제품번호id?), (알트값, 유알엘), (사이즈)
from users.models           import User, Cart
from zara.settings          import SECRET_KEY, ALGORITHM
from core.utils             import SigninDecorator


class UserCartView(View):
    @SigninDecorator
    def post(self, request):
        try:
            #유저 정보가 맞으면,
            data           = json.loads(request.body)
            user           = request.user  # ---> 로그인 데코레이터에서 불러온 유저 정보
            product        = Product.objects.get(id=data['id'])  # ---> body에 담겨온 상품의 id 값으로 불러오는게 깜끔?
            size           = Size.objects.get(name=data['size'])  # --> body에는 size라고 담겨있지만, size 모델클래스에는 name이라는 필드로 적혀있음()
            color          = Color.objects.get(name=data['color'])  # ---> body에는 color라고 담겨있지만, color 모델클래스에는 name이라는 필드로 적혀있음
            quantity       = data['quantity']  # --> body에 quantity로 담겨진 걸 변수에 다시 담음
            product_option = product.productoption_set.filter(   # ---> products가 참조 하고 있는 프로덕트옵션은 역참조를 하고 있기에, _set을 하고, 옵션에서 불러와야하는게 사이즈랑 컬러므로 위에서 변수에 저장한 color와 size를 넣는것..?
                size  = size,
                color = color
            )[0]  #---> 변수 product_option 은 객체가 아닌 쿼리셋으로 나오므로, 하나의 사이즈의 하나의 컬러는 한개뿐이므로 쿼리셋의 첫번쨔 인덱스를 불러와주기위해 [0]이 나옴
            url = ProductImage.objects.get(url=data['id'])
            # size햣 
            # 상품의 장바구니를 담아라(담고 있어야 하는 정보6가지)
            
            # 담은 장바구니를 한개의 이미지를 삭제한다면, 장바구니의 이미지만 삭제
            
            # 딤은 장바구니를 모두 삭제하기 버튼을 누른다면, 장바구니의 모두 삭제

            if quantity >= product_option.stock:
                return JsonResponse({'message' : 'OUT_OF_STOCK'}, status = 404)

            Cart.objects.create(
                user           = user,
                product_option = product_option,
                quantity       = quantity
                    # 상품이름 : 
                    # 가격 :
                    # 이미지유알에 : 
                    # 이미지알트값 :
                    # 제품번호 : 
                    # 사이즈 : 
            )
            return JsonResponse({'message' : 'SUCCESS'}, status= 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status= 401)

class CartProductEmptyView(View):
    def post(self, request):
         # 담은 장바구니를 한개의 이미지를 삭제한다면, 장바구니의 이미지만 삭제
        