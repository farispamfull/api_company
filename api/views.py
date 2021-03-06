from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Worker, User, AccessPrivilege
from .permissions import IsAdminOrDelegate, WorkersPermissions, IsAdministrator
from .serializers import (CompanySerializer, WorkerPostSerializer,
                          WorkerSerializer, RightsSerializer,
                          AccessPrivilegeSerializer, MeSerializer)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated & IsAdministrator]
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',
                     'workers__name', 'workers__work_phone',
                     'workers__personal_phone', 'workers__fax_phone'
                     ]

    def perform_create(self, serializer):
        serializer.save(administrator=self.request.user)


class BaseCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class WorkerViewSet(viewsets.ModelViewSet):
    permission_classes = [WorkersPermissions & IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'work_phone', 'fax_phone', 'personal_phone']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return WorkerSerializer
        return WorkerPostSerializer

    def get_queryset(self):
        queryset = Worker.objects.filter(company=self.kwargs.get('company_id'))
        return queryset

    def perform_create(self, serializer):
        company = get_object_or_404(Company, pk=self.kwargs.get('company_id'))
        serializer.save(company=company)


class PrivilegeView(APIView):
    permission_classes = [IsAdminOrDelegate & IsAuthenticated]

    def get(self, request, company_id):
        company = company_id
        company = get_object_or_404(Company, pk=company)
        serializer = RightsSerializer(company)
        return Response(serializer.data)

    def post(self, request, company_id):
        email = request.data.get('email')
        company = get_object_or_404(Company, pk=company_id)
        if User.objects.filter(email=email, company=company):
            return Response({"email": '?????????? ???????? ?????? ????????'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email=email)
        items = AccessPrivilege(company=company, user=user)
        items.save()
        serializer = AccessPrivilegeSerializer(items)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, company_id):
        email = request.data.get('email')
        company = get_object_or_404(Company, pk=company_id,
                                    administrator=request.user)
        if request.user.email == email:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, email=email)
        items = get_object_or_404(AccessPrivilege, company=company, user=user)
        items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    def get(self, request):
        user = request.user
        serializer = MeSerializer(user)
        return Response(serializer.data)
