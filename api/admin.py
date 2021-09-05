# Register your models here.
from django.contrib import admin

from .models import Company, Worker, AccessPrivilege


@admin.register(Company)
class AdminCategory(admin.ModelAdmin):
    empty_value_display = '-empty-'


@admin.register(AccessPrivilege)
class AdminCategory(admin.ModelAdmin):
    empty_value_display = '-empty-'


#
# @admin.register(User)
# class AdminCategory(admin.ModelAdmin):
#     empty_value_display = '-empty-'


@admin.register(Worker)
class AdminCategory(admin.ModelAdmin):
    empty_value_display = '-empty-'
