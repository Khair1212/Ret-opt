from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from .views import UserView, PasswordResetView, PasswordConfirmView, AccountActiveOrResetView, TokenPairView

router = SimpleRouter()
router.register('users', UserView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account_active_reset/<str:umail>/', AccountActiveOrResetView.as_view(), name='account_active_reset'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('confirm-password/<str:umail>/<int:otp>/', PasswordConfirmView.as_view(), name='confirm_password')
]
