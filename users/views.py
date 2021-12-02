import json,re, bcrypt

from django.http.response import JsonResponse
from django.views import View

from .models      import User

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user_name     = data['name'],
            user_email    = data['email'],
            user_password = data['password']
            
            #이메일 정규식 : '^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$'
            #패스워드 정규식 : "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$" #최소 8자~ , 문자, 숫자

            #if 이메일 정규식이 맞지 않다면(8자이상, 문자, 숫자):
            if not re.match('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$', user_email):
                return JsonResponse({"ERROR" : "EMAIL_ERROR"}, status = 400)

            #if 이메일이 이미 존재한다면:
            if User.objects.filter(email = user_email).exists:
                return JsonResponse({"ERROR" : "EMAIL_ALLEADY_EXIST"}, status=400)
        
            #if 패스워드 정규식이 맞지 않다면:
            if not re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", user_password):
                return JsonResponse({"ERROR" : "PASSWORD_ERROR"}, status = 400) 

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt().endcode('urt-8'))
            User.objects.create(
                name     = user_name,
                email    = user_email,
                password = hashed_password
                )
            return JsonResponse({"RESULT" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"ERROR" : "KEY_ERROR"}, status = 400)