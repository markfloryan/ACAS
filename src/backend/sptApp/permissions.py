from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

# Check if the user is a professor user
class IsProfessor(permissions.BasePermission):
    def has_permission(self,request,view):
        is_prof = hasattr(request.user,'is_professor') and request.user.is_professor == True
        #print("Is professor:", is_prof, flush=True)
        return is_prof

# Check if the object is associated with the user
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #print("Checking is owner", flush=True)
        is_owner = False
        if hasattr(obj,"user"): # Check for a user attribute on the objct
            is_owner = (obj.user == request.user)
        elif hasattr(obj,"student"): # Check for student attribute on the object
            is_owner = (obj.student == request.user)
        #print("IS OWNER:",is_owner,flush=True)
        return is_owner

# Only allow reads
class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

# Only allow posts
class CreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"