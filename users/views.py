import json, bcrypt, jwt

from django.http.response   import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View

from users.validation       import email_check, password_check
from zara.settings          import SECRET_KEY, ALGORITHM
from .models                import User

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
            return JsonResponse({'MESSAGE' : 'EMAIL_INVALD_USER'}, status=401)