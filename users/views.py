import json, bcrypt, jwt

from django.http.response   import JsonResponse
from django.core.exceptions import ValidationError  #커스텀 에러 

from django.views           import View
from .models                import User
from .validation            import *

from zara.settings import SECRET_KEY

class LoginView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user_email    = data['email']
            user_password = data['password']
            user_db       = User.objects.get(email = user_email)
            
            #if DB에 입력받은 이메일과 패스워드가 없다면 :
            if user_db.email != user_email and user_db.password != user_password:
                return JsonResponse({'ERROR' : 'INVALD_USER'}, status=401)
            
            #if DB에 입력받은 이메일이 없다면 :
            #if user_db.email != user_email:
            #    return JsonResponse({'ERROR' : 'INVALD_ERROR'}, status=400)

            #if DB에 입력받은 패스워드가 없다면:
            #if user_db.password != user_password:
            #    return JsonResponse({'ERROR' : 'INVALD_ERROR'}, status=400)

            #올바른 이메일과 패스워드 입력하면
            #리턴 토큰발행
            
            if bcrypt.checkpw(user_password.encode('utf-8'), user_db.password.decode('utf-8')):
                token = jwt.encode({'user_id': user_db.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'MESSAGE' : 'SUCCESS', 'ACCESS_TOKEN' : token}, status=200)
            return JsonResponse({'ERROR' : 'INVAILD_USER'}, status=401)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)
        
