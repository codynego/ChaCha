from rest_framework import permissions

class IsParticipantPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.sender or request.user == obj.receiver:
            return True
        return False
    