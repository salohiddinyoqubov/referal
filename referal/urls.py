from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SendCodeViewSet, VerifyCodeViewSet, ReferalViewSet, ReferalConfirmViewSet

router = DefaultRouter()
router.register(r'send-code', SendCodeViewSet, basename='send-code')
router.register(r'verify-code', VerifyCodeViewSet, basename='verify-code')
router.register(r'referal', ReferalViewSet, basename='referal')
router.register(r'referal-confirm', ReferalConfirmViewSet, basename='referal-confirm')

urlpatterns = [
    path('', include(router.urls)),
]
