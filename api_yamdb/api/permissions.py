from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Пользователь является админом и он авторизован."""
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsModerOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять комментарии, отзывы только авторам
    или модератору.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
    
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                )
            )
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
