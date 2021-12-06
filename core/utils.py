import json, jwt, os

from django.http            import JsonResponse

from zara.settings          import SECRET_KEY
from users.models           import User

def SigninDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET_KEY, algorithms=os.environ["ALGORITHM"])
            user         = User.objects.get(id = payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'ERROR':'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'ERROR' : 'INVALID_USER'}, status=400)
            
        return func(self, request, *args, **kwargs)

    return wrapper