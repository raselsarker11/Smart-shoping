from django.urls import path
from .views import RegisterView, LogOutAPIView, MyProtectedView, CustomTokenIssuanceView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogOutAPIView.as_view(), name='logout_view'),
    path('protected/', MyProtectedView.as_view(), name='protected-view'),
    path('issue-access-token/', CustomTokenIssuanceView.as_view(), name='issue_access_token'),
]
