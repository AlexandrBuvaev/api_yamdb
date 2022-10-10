from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только автор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
        # return request.user.role == 'MODERATOR'


class IsModerOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только модератор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'MODERATOR'


class IsAdminOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только админ."""

    def has_permission(self, request, view, obj):
        return request.user.role == 'ADMIN' or request.user.is_staff or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только админ."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'ADMIN'


class IsReadOnly(permissions.BasePermission):
    """Класс пермишена чтения всем."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
