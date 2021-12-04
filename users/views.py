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
            # 입력받은 유저의 이메일이 없는지 확인할 수 잇는 방법1)
            data          = json.loads(request.body)
            user_email    = data['email'] #--> 입력받은 request.body의 email라는 키의 value값을 불러온것
            user_password = data['password']
            user_db       = User.objects.get(email = user_email)  #--> DB에 입력된 정보를 변수 user_db에 담은것 
                                                                  #--> 여기 get메소드를 통해서 입력받은 email이 없으면 바로 에러가 발생함(doesnotexist에러 발생) 
                                                                  #    그래서 doesnotexist 에러 메세지를 따로 지정해 줘야함
            if bcrypt.checkpw(user_password.encode('utf-8'), user_db.password.encode('utf-8')):
                token = jwt.encode({'user_id': user_db.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'MESSAGE' : 'SUCCESS', 'ACCESS_TOKEN' : token}, status=200)
            return JsonResponse({'ERROR' : 'PASSWORD_INVAILD_USER'}, status=401)
                                 
        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'EMAIL_INVALD_USER'}, status=401)

        # try:
        #     # 입력받은 유저의 이메일이 없는지 확인할 수 잇는 방법2)
        #     data          = json.loads(request.body)
        #     user_email    = data['email'] #--> 입력받은 request.body의 emial만 불러온것 
        #     user_password = data['password']
            
        #     if not User.objects.filter(email=user_email).exists():
        #         return JsonResponse({'ERROR' : 'EMAIL_INVALD_USER'}, status=401)
            
        #     user_db = User.objects.get(email = user_email) # --> filter를 통해서 이메일 존재여부를 확인했으니, 비번에 대한 DB 여부를 확인할 변수를 지정함
            
        #     if bcrypt.checkpw(user_password.encode('utf-8'), user_db.password.encode('utf-8')):
        #         token = jwt.encode({'user_id': user_db.id}, SECRET_KEY, algorithm = 'HS256')
        #         return JsonResponse({'MESSAGE' : 'SUCCESS', 'ACCESS_TOKEN' : token}, status=200)
        #     return JsonResponse({'ERROR' : 'PASSWORD_INVAILD_USER'}, status=401)
                                 
        # except KeyError:
        #     return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)
