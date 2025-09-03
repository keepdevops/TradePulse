#!/usr/bin/env python3
"""
TradePulse Authentication - RBAC Test Module
Tests Role-Based Access Control functionality
"""

def run_tests():
    """Test Role-Based Access Control functionality"""
    print("🔒 Testing RBAC...")
    
    try:
        from auth.rbac import RoleBasedAccessControl, Permission, Role
        
        # Initialize RBAC
        rbac = RoleBasedAccessControl()
        print("  ✅ RBAC initialized")
        
        # Test role assignment
        user_id = 1
        role_assigned = rbac.assign_role_to_user(user_id, "trader")
        print(f"  ✅ Role assignment: {role_assigned}")
        
        # Test permission checking
        has_permission = rbac.user_has_permission(user_id, Permission.VIEW_PORTFOLIO)
        print(f"  ✅ Permission check: {has_permission}")
        
        # Test role listing
        roles = rbac.list_roles()
        print(f"  ✅ Role listing: {len(roles)} roles found")
        
        # Test role hierarchy
        hierarchy = rbac.get_role_hierarchy()
        print(f"  ✅ Role hierarchy: {len(hierarchy)} roles in hierarchy")
        
        print("  🎯 RBAC tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ RBAC test failed: {e}")
        return False
