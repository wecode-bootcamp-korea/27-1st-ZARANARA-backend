import jwt

from django.http    import JsonResponse

from zara.settings  import SECRET_KEY, ALGORITHM
from users.models   import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            request.user = User.objects.get(id = payload['user_id'])

        except jwt.exceptions.DecodeError:
            return JsonResponse({'ERROR':'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'ERROR' : 'INVALID_USER'}, status=400)
            
        return func(self, request, *args, **kwargs)
    return wrapper

def signin_check_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)

            if not token:
                request.user = None
                return func(self, request, *args, **kwargs)
                
            payload      = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            request.user = User.objects.get(id = payload['user_id'])
            
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'ERROR':'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'ERROR' : 'INVALID_USER'}, status=400)
    return wrapper

