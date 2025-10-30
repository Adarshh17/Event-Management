from rest_framework import permissions


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organizers of an event to edit or delete it.
    Read-only permissions are allowed for any request.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the organizer of the event
        return obj.organizer == request.user


class IsInvitedOrPublic(permissions.BasePermission):
    """
    Custom permission to restrict access to private events.
    Only invited users or the organizer can view private events.
    Public events are accessible to everyone.
    """
    
    def has_object_permission(self, request, view, obj):
        # If event is public, allow access
        if obj.is_public:
            return True
        
        # If user is not authenticated, deny access to private events
        if not request.user.is_authenticated:
            return False
        
        # If user is the organizer, allow access
        if obj.organizer == request.user:
            return True
        
        # For private events, you could add invitation logic here
        # For now, we'll deny access to all other users
        # You could extend this to check an Invitation model:
        # return Invitation.objects.filter(event=obj, user=request.user).exists()
        
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only permissions are allowed for any request.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user
