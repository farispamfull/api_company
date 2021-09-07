from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Company


class IsAdminOrDelegate(BasePermission):

    def has_permission(self, request, view):
        company_id = request.resolver_match.kwargs.get('company_id')
        if Company.objects.filter(pk=company_id,
                                  administrator=request.user.id).exists():
            return True
        if request.method == "GET":
            if Company.objects.filter(pk=company_id,
                                      delegate_persons=request.user).exists():
                return True
        return False


class IsAdministrator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.administrator == request.user


class WorkersPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        company_id = request.resolver_match.kwargs.get('company_id')

        if Company.objects.filter(pk=company_id,
                                  administrator=request.user.id).exists():
            return True

        if Company.objects.filter(pk=company_id,
                                  delegate_persons=request.user).exists():
            return True
        return False
