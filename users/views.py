import json, bcrypt, jwt
from json.decoder import JSONDecodeError
import re

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
                return JsonResponse({"MESSAGE" : "EMAIL_ALREADY_EXIST"}, status=400)
        
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
            return JsonResponse({'MESSAGE' : v.message}, status=401)


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
            return JsonResponse({'MESSAGE' : 'EMAIL_INVALD_USER'}, status=400)

class UserCartView(View):
    #장바구니 담기 기능 구현
    #유저 정보를 가진 사람인지 아닌지 먼저 판단하기
    #json에 담길 정보(받아올것)는 ? product정보랑 수량 
    #물품정보를 
    #카트에 담을 정보(user -> class User 참조, product -> class Product 참조, quantity -> 숫자로)
    #성공메세지
    #실패메세지

    #목적 : 받은 유저 정보로 물품의 정보 담기 

    @signin_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            #물품 정보를 받을 것
            user       = request.user
            print(1)
            product_id = data['product_id'] # --> 키값을 product로 정해도 되나, 정확히 어떤 정보를 갖고 올건지...name price도 좋으나 중복값이 없는 id값이 명확해서 좋음 --> httpie 통신(프론트 통신)할때도 키값을 맞추기
            print(2)
            quantity   = data['quantity']
            #유저 정보 담긴 무엇가
            
            print(3)
            Cart.objects.create(
                user     = User.objects.get(id = user.id),
                product  = Product.objects.get(id = product_id),
                quantity = quantity 
            )
            return JsonResponse({'message':'success'}, status=201) 
        except KeyError:
            return JsonResponse({'message':'keyerror'}, status=400)

        except JSONDecodeError: # --> 500에러 뜸 / Cart 생성할때, 키값과 벨류값 안주고 토근만 넘겨줄때 발생한 에러(header에 있는 토큰값만 주고 body에 넘겨줄 키값과 벨류값이 없어서 발생하는 에러 : 즉, 토큰과 함께 body에 담겨줄 정보를 넘겨주면 에러 해결)
            return JsonResponse({'message':'body '}, status=400) # --> 제이슨디코드에러를 설정했더니 갑자기 200 코드 발생...난 아무것도 상태코드를 넣지 않앟ㅆ는데...(아직 status코드를 내가 작성하지 않아서 defalt값인 200상태 코드가 뜨는것, 적절한 상태 코드 넣으면 해결)

