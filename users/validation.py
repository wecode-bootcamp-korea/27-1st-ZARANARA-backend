import re

from django.core.exceptions import ValidationError

def email_check(value):
    if not re.match('([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})', value):
        raise ValidationError("EMAIL_ERROR")

def password_check(value):
    if not re.match("(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}", value):
        raise ValidationError("PASSWORD_ERROR")

