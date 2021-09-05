from django.db.models import Q
from operator import itemgetter
from rest_framework import serializers

from .models import Company, Worker, User, AccessPrivilege


class WorkerPostSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    def validate_name(self, value):
        worker = Worker.objects.filter(
            name=value,
            company=self.context['view'].kwargs[
                'company_id'])
        if worker:
            raise serializers.ValidationError('Такой работник уже есть')
        return value

    def validate_personal_phone(self, value):
        worker = Worker.objects.filter(
            personal_phone=value,
            company=self.context['view'].kwargs[
                'company_id'])
        if worker:
            raise serializers.ValidationError('Номер уже занят')
        return value

    def validate(self, attrs):
        item = Worker(**attrs)
        if item.clean():
            return attrs
        raise serializers.ValidationError('Нужно ввести хотя бы один номер')

    class Meta:
        model = Worker
        fields = (
            'company', 'name', 'position', 'personal_phone',
            'fax_phone',
            'work_phone')


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        search = None
        pre_search = self.context['request'].GET
        if 'search' in pre_search:
            search = pre_search['search']

        if search:
            data = data.filter(
                Q(name__icontains=search) | Q(work_phone__icontains=search) |
                Q(fax_phone__icontains=search) | Q(
                    personal_phone__icontains=search))[:5]

        return super(FilteredListSerializer, self).to_representation(data)


class WorkerSerializer(serializers.ModelSerializer):
    phones = serializers.SerializerMethodField(method_name='get_phones')

    def get_phones(self, obj):
        data = obj.get_phones()
        data = dict(filter(itemgetter(1), data.items()))
        return data

    class Meta:
        model = Worker
        fields = (
            'id', 'name', 'position', 'phones')
        list_serializer_class = FilteredListSerializer


class CompanySerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'address', 'workers')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RightsSerializer(serializers.ModelSerializer):
    delegate_persons = UserSerializer(many=True, read_only=True)
    administrator = UserSerializer()

    class Meta:
        model = Company
        fields = ('administrator', 'delegate_persons',)


class AccessPrivilegeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    class Meta:
        model = AccessPrivilege
        fields = ('company', 'user')


class MeCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')
 

class MePrivilegeSerializer(serializers.ModelSerializer):
    company = MeCompanySerializer(read_only=True)

    class Meta:
        model = AccessPrivilege
        fields = ('company',)


class MeSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(
        method_name='get_permissions')

    companies = serializers.SerializerMethodField(
        method_name='get_companies')

    def get_companies(self, obj):
        data = obj.companies
        company = MeCompanySerializer(data, many=True)
        return company.data

    def get_permissions(self, obj):
        data = obj.permissions
        company = MePrivilegeSerializer(data, many=True)
        return company.data

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'permissions', 'companies')
