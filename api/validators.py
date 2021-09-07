import re

from django.core.exceptions import ValidationError


def validate_name(name):
    if len(name.split()) != 3:
        raise ValidationError(
            f'<{name}>  необходимо указать ФИО')


def validate_phone(phone):
    reg = re.compile('^\+\d{8,15}$')
    if not reg.match(phone):
        raise ValidationError(
            f'<{phone}>  неверно введен номер')



