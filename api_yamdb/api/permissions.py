from rest_framework import permissions


class IsAuthorAdminModerOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только автор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsModerOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только модератор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'moderator'


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только админ."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'
