from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Пользователь является админом и он авторизован."""
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только автор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsModerOrReadOnly(permissions.BasePermission):
    """
    Проверка на разрешение для изменения.
    Изменять может только модератор.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_moderator)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только админ."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin


class IsAdminOrReadOnlyGet(permissions.BasePermission):
    """Проверка на разрешение для изменения. Изменять может только админ."""
    # def has_permission(self, request, view):
    #     return (
    #         request.user.is_admin
    #         or request.method in ["GET", "POST", "DELETE"]
    #     )

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", ]:
            return True
        return request.user.role == 'admin' and request.method in ["POST", "DELETE"]
