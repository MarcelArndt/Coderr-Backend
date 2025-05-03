from rest_framework import permissions
from coderr_market_app.models import Profiles
from django.shortcuts import get_object_or_404

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if hasattr(obj, 'user') and obj.user:
            return request.user.id == getattr(obj.user, 'id', obj.user)
        elif hasattr(obj, 'customer_user') and obj.customer_user:
            return request.user.id == obj.customer_user
        elif hasattr(obj, 'business_user') and obj.business_user:
            return request.user.id == obj.business_user
        
    
class IsReviewerOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        reviewer_profile = obj.reviewer
        return request.user == reviewer_profile.user


class IsOrderOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        business_profile = getattr(obj, 'offersDetails', None)
        if business_profile:
            business_profile = getattr(obj.offersDetails, 'offer', None)
        if business_profile:
            business_user_profile = obj.offersDetails.offer.user  
            return request.user == business_user_profile.user
        return False
    
class IsBusiness(permissions.BasePermission):
     def has_permission(self, request, view):
        profil = get_object_or_404(Profiles, user=request.user)
        return profil.type == "business"
     
class IsCustomer(permissions.BasePermission):
     def has_permission(self, request, view):
        profil = get_object_or_404(Profiles, user=request.user)
        return profil.type == "customer"
        

    
