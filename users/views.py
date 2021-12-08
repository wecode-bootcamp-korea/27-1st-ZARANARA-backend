import json, bcrypt, jwt

from django.http.response   import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View

from users.validation       import email_check, password_check
from zara.settings          import SECRET_KEY, ALGORITHM
from core.utils             import signin_decorator

from products.models        import Color, Product, ProductImage, ProductOption, Size 
from .models                import User, Cart

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user_name     = data['name']
            user_email    = data['email']
            user_password = data['password']
            
            email_check(user_email)

            if User.objects.filter(email = user_email).exists():
                return JsonResponse({"MESSAGE" : "EMAIL_ALLEADY_EXIST"}, status=400)
        
            password_check(user_password)

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            User.objects.create(
                name     = user_name,
                email    = user_email,
                password = hashed_password
            )
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

        except ValidationError as v:
            return JsonResponse({'MESSAGE' : v.message}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user_email    = data['email'] 
            user_password = data['password']
            user_db       = User.objects.get(email = user_email)  

            if bcrypt.checkpw(user_password.encode('utf-8'), user_db.password.encode('utf-8')):
                token = jwt.encode({'user_id' : user_db.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({'MESSAGE' : 'SUCCESS', 'ACCESS_TOKEN' : token}, status=200)
            return JsonResponse({'MESSAGE' : 'PASSWORD_INVAILD_USER'}, status=401)
            
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'EMAIL_INVALD_USER'}, status=401)

#                         (이름, 가격, 제품번호id?), (알트값, 유알엘), (사이즈)
class UserCartView(View):
    @signin_decorator
    def post(self, request):
        try:
            #유저 정보가 맞으면,
            data           = json.loads(request.body)
            user           = request.user  # ---> 로그인 데코레이터에서 불러온 유저 정보
            product        = Product.objects.get(id=data['id'])  # ---> body에 담겨온 상품의 id 값으로 불러오는게 깜끔?
            size           = Size.objects.get(name=data.get('size','ONE SIZE'))  # --> body에는 size라고 담겨있지만,       size 모델클래스에는 name이라는 필드로 적혀있음()
            color          = Color.objects.get(name=data.get('color', 'ONE COLOR'))  # ---> body에는 color라고 담겨있지만, color 모델클래스에는 name이라는 필드로 적혀있음
            quantity       = data.get('quantity',1) # --> body에 quantity로 담겨진 걸 변수에 다시 담음
            product_option = product.productoption_set.filter(   # ---> products가 참조 하고 있는 프로덕트옵션은 역참조를 하고 있기에, _set을 하고, 옵션에서 불러와야하는게 사이즈랑 컬러므로 위에서 변수에 저장한 color와 size를 넣는것..?
                size  = size,
                color = color
            )[0]  #---> 변수 product_option 은 객체가 아닌 쿼리셋으로 나오므로, 하나의 사이즈의 하나의 컬러는 한개뿐이므로 쿼리셋의 첫번쨔 인덱스를 불러와주기위해 [0]이 나옴
            
            # size햣 
            # 상품의 장바구니를 담아라(담고 있어야 하는 정보6가지)
            
            # 담은 장바구니를 한개의 이미지를 삭제한다면, 장바구니의 이미지만 삭제
            
            # 딤은 장바구니를 모두 삭제하기 버튼을 누른다면, 장바구니의 모두 삭제

            # if quantity >= product_option.stock:
            #     return JsonResponse({'message' : 'OUT_OF_STOCK'}, status = 404)
            if Cart.objects.filter(user=user, product_option=product_option).exists():
                return JsonResponse({'message' : 'ITEM_ALREADY_EXIST'}, status=400)
                
            Cart.objects.create(
                user           = user,
                product_option = product_option,
                quantity       = quantity
            )

            return JsonResponse({'message' : 'SUCCESS'}, status= 200)

        except KeyError: 
            return JsonResponse({'message' : 'KEY_ERROR'}, status= 401)

        except Product.DoesNotExist: 
            return JsonResponse({'message':'DOESNOTEXIST'}, status = 401)

    @signin_decorator
    def get(self, request):
        cart_list = Cart.objects.filter(user_id=request.user)
        
        result=[
           {
             "color"   : cart.product_option.color.name,
             "size"    : cart.product_option.size.name,
             "image"   : cart.product_option.product.productimage_set.all()[0].url,
             "alt"     : cart.product_option.product.productimage_set.all()[0].alt,
             "name"    : cart.product_option.product.name,
             "price"   : cart.product_option.product.price,
             "id"      : cart.product_option.product.id,
             "quantity": cart.quantity,
             "cart_id" : cart.id
            }
        for cart in cart_list
        ]

        return JsonResponse({'result': result}, status=200)


    @signin_decorator
    def delete(self, request):
        cart_id = request.GET.get('cartId')
        if cart_id: 
            Cart.objects.get(id=cart_id).delete()
            return JsonResponse({'message':'ITEM_DELETE_SUCCESS'},status = 200)

        if not Cart.objects.filter(user=request.user).exists(): 
            return JsonResponse({'message':'OUT_OF_ITEMS'}, status = 400)

        Cart.objects.filter(user=request.user).delete()
        return JsonResponse({'message':'TOTAL_DELETE_SUCCESS'},status = 200)
    


    @signin_decorator
    def patch(self, request):
        try:
            data            = json.loads(request.body)
            # quantity        = data['quantity']
            cart_id         = data['cart_id']
            cart            = Cart.objects.get(id=cart_id, user_id=request.user)

            if data['option'] == 'plus':
                cart.quantity += 1
            else:
                cart.quantity -= 1

            cart.save()
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'OBJECT_NOT_EXITST'}, status=400)


    # 저기서 오는 수량 과 스톡 비교 
    # 스톡보다 많으면 오류 반환
    # 가격도 불러와서 수량과 곱하기







# class CartView(View):
#     @signin_decorator
#     def get(self, request):
#         #장바구니 보여줄것
#         #request.user -> 유저객체
#         #카트 테이블에 해당 유저가 들어있는 모든 객체가져오기
#         cart_list = Cart.objects.filter(user_id=request.user)
#         cart_list[0].productoption.all




#         #카드 : 프로덕트 옵션아이디, 유저아이디
#         ({

#         })
        
        # 상품이름 : 
                    # 가격 :
                    # 이미지유알에 : 
                    # 이미지알트값 :
                    # 제품번호 : 
                    # 사이즈 : 
         # 담은 장바구니를 \






# # def 장바구니 담은 합계
# class CartProductEmptyView
# # def 장바구니 부분 삭제

# # def 장바구니 전체 바우는