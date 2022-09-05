from rest_framework import permissions


class OnlyAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated


class Owner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
