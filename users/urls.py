from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, ProfileView,SendSMSOTPView, VerifySMSOTPView,ManageAdminsView, ManageStaffView, ManageDesignersView, ReportsView
from .views import CustomTokenObtainPairView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('send-otp/', SendSMSOTPView.as_view(), name='send-sms-otp'),
    path('verify-otp/', VerifySMSOTPView.as_view(), name='verify-sms-otp'),
    # Owner
    path('admins/', ManageAdminsView.as_view(), name='manage-admins'),
    path('admins/<int:pk>/', ManageAdminsView.as_view(), name='manage-admin-detail'),

    # Admin & Owner
    path('staff/', ManageStaffView.as_view(), name='manage-staff'),
    path('staff/<int:pk>/', ManageStaffView.as_view(), name='manage-staff-detail'),
    path('reports/', ReportsView.as_view(), name='reports'),

    # Staff & Above
    path('designers/', ManageDesignersView.as_view(), name='manage-designers'),
    path('designers/<int:pk>/', ManageDesignersView.as_view(), name='manage-designer-detail'),
]
