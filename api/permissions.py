from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Company


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.get('company_id') == 2


class IsAuthenticatedOrReadOnly(BasePermission):


    def has_permission(self, request, view):
        company_id = request.resolver_match.kwargs.get('company_id')
        print(request.user, request.user.id)
        if Company.objects.filter(pk=company_id,
                                  administrator=request.user.id).exists():
            return True
        if request.method == "GET":
            if Company.objects.filter(pk=company_id,
                                      delegate_persons=request.user).exists():
                return True
        return False


class WorkersPermissions(BasePermission):


    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        company_id = request.resolver_match.kwargs.get('company_id')
        print(request.user, request.user.id)

        if Company.objects.filter(pk=company_id,
                                  administrator=request.user.id).exists():
            return True

        if Company.objects.filter(pk=company_id,
                                  delegate_persons=request.user).exists():
            return True
        return False
