from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from .utils import send_sms_otp, verify_sms_otp
from .permissions import IsOwner, IsAdminOrOwner, IsStaffOrAbove
User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Logged out successfully'},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
class SendSMSOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=400)
        try:
            send_sms_otp(phone_number)
            return Response({'message': 'OTP sent successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class VerifySMSOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        if not phone_number or not otp:
            return Response({'error': 'Phone number and OTP are required'}, status=400)
        if verify_sms_otp(phone_number, otp):
            return Response({'message': 'OTP verified successfully', 'verified': True})
        return Response({'error': 'Invalid or expired OTP', 'verified': False}, status=400)
# ── Owner Only — Manage Admins ──

class ManageAdminsView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        admins = User.objects.filter(role='admin')
        serializer = UserSerializer(admins, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk, role='admin')
        user.delete()
        return Response({'message': 'Admin deleted'})


# ── Admin & Owner — Manage Staff ──

class ManageStaffView(APIView):
    permission_classes = [IsAdminOrOwner]

    def get(self, request):
        staff = User.objects.filter(role='staff')
        serializer = UserSerializer(staff, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = User.objects.get(pk=pk, role='staff')
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk, role='staff')
        user.delete()
        return Response({'message': 'Staff deleted'})


# ── Staff & Above — Manage Designers ──

class ManageDesignersView(APIView):
    permission_classes = [IsStaffOrAbove]

    def get(self, request):
        designers = User.objects.filter(role='designer')
        serializer = UserSerializer(designers, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        designer = User.objects.get(pk=pk, role='designer')
        serializer = UserSerializer(designer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# ── Admin & Owner — Reports ──

class ReportsView(APIView):
    permission_classes = [IsAdminOrOwner]

    def get(self, request):
        data = {
            'total_users': User.objects.count(),
            'total_customers': User.objects.filter(role='customer').count(),
            'total_designers': User.objects.filter(role='designer').count(),
            'total_staff': User.objects.filter(role='staff').count(),
            'total_admins': User.objects.filter(role='admin').count(),
        }
        return Response(data)
# ── Custom JWT Login — returns user data with token ──
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'phone': self.user.phone,
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer