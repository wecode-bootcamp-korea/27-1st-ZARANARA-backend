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
    @signin_decorator
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user_id        = request.user
            product_id     = Product.objects.get(id=data['product_id'])
            quantity       = data['quantity']
            
            if Cart.objects.filter(user=user_id, product=product_id).exists():
                return JsonResponse({'MESSAGE' : 'ITEM_ALREADY_EXIST'}, status=400)
                
            Cart.objects.create(
                user     = user_id,
                product  = product_id,
                quantity = quantity
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status= 201)

        except KeyError: 
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status= 400)

        except Product.DoesNotExist: 
            return JsonResponse({'MESSAGE' : 'DOES_NOT_EXIST'}, status = 401)

    @signin_decorator
    def get(self, request):
        cart_list = Cart.objects.filter(user_id=request.user)
        
        result=[
           {
             "image"     : cart.product.productimage_set.all()[0].url,
             "alt"       : cart.product.productimage_set.all()[0].alt,
             "name"      : cart.product.name,
             "price"     : cart.product.price,
             "product_id": cart.product.id,
             "quantity"  : cart.quantity,
             "cart_id"   : cart.id
            }
        for cart in cart_list
        ]

        return JsonResponse({'result': result}, status=200)


    @signin_decorator
    def delete(self, request):
        cart_id = request.GET.get('cartId')

        if cart_id: 
            Cart.objects.get(id=cart_id).delete()
            return JsonResponse({'MESSAGE':'ITEM_DELETED'},status = 200)

        if not Cart.objects.filter(user=request.user).exists(): 
            return JsonResponse({'MESSAGE':'DOES_NOT_EXIST'}, status = 400)

        Cart.objects.filter(user=request.user).delete()
        return JsonResponse({'MESSAGE':'ALL_DELETED'},status = 200)
    


    @signin_decorator
    def patch(self, request):
        try:
            data          = json.loads(request.body)
            quantity      = data['quantity']
            cart_id       = data['cart_id']
            cart          = Cart.objects.get(id=cart_id, user_id=request.user)
            cart.quantity = int(quantity)

            cart.save()
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'OBJECT_NOT_EXITST'}, status=400)