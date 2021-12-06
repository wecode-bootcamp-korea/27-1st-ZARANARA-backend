import json, bcrypt

from django.http.response   import JsonResponse
from django.core.exceptions import ValidationError 
from django.views           import View

from users.validation       import email_check, password_check

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
                return JsonResponse({"ERROR" : "EMAIL_ALLEADY_EXIST"}, status=400)
        
            password_check(user_password)

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            User.objects.create(
                name     = user_name,
                email    = user_email,
                password = hashed_password
            )
            return JsonResponse({"RESULT" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"ERROR" : "KEY_ERROR"}, status = 400)

        except ValidationError as v:
            return JsonResponse({'ERROR' : v.message}, status=400)