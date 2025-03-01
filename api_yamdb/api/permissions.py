from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsAdminModeratorAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj): 
        return (request.method in SAFE_METHODS or obj.author == request.user
                or request.user.is_moderator_or_admin())


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or super().has_permission(request, view))
