from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Only owner can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

class IsAdminOrOwner(BasePermission):
    """Admin and owner can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'owner']

class IsStaffOrAbove(BasePermission):
    """Staff, admin and owner can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['staff', 'admin', 'owner']

class IsDesigner(BasePermission):
    """Only designers can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'designer'

class IsCustomer(BasePermission):
    """Only customers can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'