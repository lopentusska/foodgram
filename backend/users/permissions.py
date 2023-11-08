from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):
    """Custom permissions for users and recipes urls."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ('users',):
            if request.method in ['GET']:
                return bool(request.user and request.user.is_authenticated)
            return bool(request.user == obj and request.user.is_authenticated)

        if view.basename in ('recipes',):
            if 'favorite' in request.path or 'shopping_cart' in request.path:
                return bool(request.user and request.user.is_authenticated)

            if request.method in ['DELETE', 'PATCH']:
                return bool(
                    request.user.is_superuser or request.user in [obj.author]
                )
            return bool(request.user and request.user.is_authenticated)

        return False

    def has_permission(self, request, view):
        if view.basename in ('users', 'recipes',):
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)

        return False
