import re

from django.core.exceptions import ValidationError

def email_check(value):
    if re.match('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$', value) is None:
        raise ValidationError("EMAIL_ERROR")

# 최소 8자 이상, 문자, 숫자
def password_check(value):
    if not re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", value):
        raise ValidationError("PASSWORD_ERROR")

