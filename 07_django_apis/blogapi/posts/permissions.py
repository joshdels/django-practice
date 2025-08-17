from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
 
    
    def has_object_permission(self, request, view, obj):
        # Granted read-only permission
        if request.method in permissions.SAFE_METHODS:
            return True

        # grated update write to the author
        return obj.author == request.user