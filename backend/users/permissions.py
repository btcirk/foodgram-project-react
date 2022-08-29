from rest_framework import permissions

class OnlyAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated