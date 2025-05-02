from rest_framework import permissions
from coderr_market_app.models import Profiles
from django.shortcuts import get_object_or_404

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True
        
        if hasattr(obj, 'user') and obj.user:
            return request.user.id == getattr(obj.user, 'id', obj.user)

        if hasattr(obj, 'customer_user') and obj.customer_user:
            return request.user.id == obj.customer_user
        elif hasattr(obj, 'business_user') and obj.business_user:
            return request.user.id == obj.business_user


        return False
    
class IsBusiness(permissions.BasePermission):
     def has_permission(self, request, view):
        profil = get_object_or_404(Profiles, user=request.user)
        return profil.type == "business"
     
class IsCustomer(permissions.BasePermission):
     def has_permission(self, request, view):
        profil = get_object_or_404(Profiles, user=request.user)
        return profil.type == "customer"
        

    
