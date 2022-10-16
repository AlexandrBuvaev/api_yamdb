from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Пользователь является админом и он авторизован."""

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает менять контент только админу в остальных
    случаях доступ только для чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAdminModerAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять объект только автору, админу
    или модератору.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
