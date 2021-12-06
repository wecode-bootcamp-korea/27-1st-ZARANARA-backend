import jwt, os

from zara.settings  import SECRET_KEY, ALGORITHM
from users.models   import User

def SigninCheckDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            # print(f"token::{token}")
            if not token:
                request.user = 0
                return func(self, request, *args, **kwargs)
            payload      = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id = payload['id'])
            request.user = user
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            request.user = 0
            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            request.user = 0
            return func(self, request, *args, **kwargs)
    return wrapper