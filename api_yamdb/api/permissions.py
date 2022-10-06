from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    """Класс пермишена чтения всем."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
