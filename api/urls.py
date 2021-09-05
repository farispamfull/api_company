from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, WorkerViewSet,PrivilegeView,MeView

router_v1 = DefaultRouter()
router_v1.register('company', CompanyViewSet)
router_v1.register(
    r'company/(?P<company_id>\d+)/workers',
    WorkerViewSet,
    basename='Worker'
)
# router_v1.register(
#     r'company/(?P<company_id>\d+)/rights',
#     RightsViewsSet, 'AccessPrivilege'
# )
urlpatterns = [
    path('v1/me/',MeView.as_view()),
    path('v1/company/<int:company_id>/access/',PrivilegeView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls'))
]
