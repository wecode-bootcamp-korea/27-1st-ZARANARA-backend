import json,re

from django.http.response import JsonResponse

def email_check(value):
    if not re.match('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$', value):
        return JsonResponse({"ERROR" : "EMAIL_ERROR"}, status = 400)