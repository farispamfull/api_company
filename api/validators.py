from django.core.exceptions import ValidationError


def validate_name(name):
    if len(name.split()) != 3:
        raise ValidationError(
            f'<{name}>  необходимо указать ФИО')
