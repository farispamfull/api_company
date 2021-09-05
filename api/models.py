from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Company(models.Model):
    administrator = models.ForeignKey(User, on_delete=models.SET_NULL,
                                      null=True,
                                      related_name='companies')
    name = models.CharField('Название компании', max_length=50, unique=True)
    description = models.TextField('Описание', null=True, blank=True)
    address = models.TextField('Адрес', null=True, blank=True)
    delegate_persons = models.ManyToManyField(User, through='AccessPrivilege')


class AccessPrivilege(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='permissions')

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company'],
                                    name='unique_permission')
        ]


class Worker(models.Model):
    company = models.ForeignKey(Company, 'Компания',
                                related_name='workers')
    name = models.CharField('ФИО', max_length=50)
    position = models.CharField('Долженость',
                                max_length=40)
    personal_phone = models.CharField(verbose_name='Личный номер',
                                      max_length=15, null=True, blank=True)
    fax_phone = models.CharField('Факс номер', max_length=15, null=True,
                                 blank=True)
    work_phone = models.CharField('Рабочий номер', max_length=15, null=True,
                                  blank=True)

    def serializer_clean(self):
        return self.fax_phone or self.work_phone or self.personal_phone

    # def clean(self):
    #     if not (self.fax_phone or self.work_phone or self.personal_phone):
    #         raise ValueError(
    #             'you must enter at least one phone number')

    def get_phones(self):
        data = {
            'personal_phone': self.personal_phone,
            'fax_phone': self.fax_phone,
            'work_phone': self.work_phone
        }
        return data

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'name'],
                                    name='unique_name'),
            # models.UniqueConstraint(fields=['company', 'personal_phone'],
            #                         name='unique_phone')
        ]
