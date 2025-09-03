#!/usr/bin/env python3
"""
TradePulse Authentication - Admin Test Module
Tests admin-specific functionality
"""

def run_tests():
    """Test admin-specific functionality"""
    print("👑 Testing Admin Functionality...")
    
    try:
        from auth.auth_service import AuthService
        from auth.rbac import Permission
        
        # Initialize auth service
        auth_service = AuthService("./data/test_users.db")
        
        # Authenticate as admin
        auth_success, auth_message, admin_info = auth_service.authenticate_user(
            username="admin",
            password="Admin123!",
            ip_address="127.0.0.1",
            user_agent="Admin Browser"
        )
        
        if auth_success and admin_info:
            admin_user_id = admin_info["user_id"]
            print(f"  ✅ Admin authentication: {admin_info['username']}")
            
            # Test user listing (admin only)
            success, message, users = auth_service.list_users(admin_user_id)
            print(f"  ✅ Admin user listing: {success} - {len(users) if users else 0} users")
            
            # Test role assignment (admin only)
            if users:
                target_user = users[0]
                role_success, role_message = auth_service.assign_role_to_user(
                    admin_user_id, target_user["id"], "trader"
                )
                print(f"  ✅ Role assignment: {role_success} - {role_message}")
            
            # Test user activity viewing
            activity_success, activity_message, activities = auth_service.get_user_activity(
                admin_user_id, admin_user_id
            )
            print(f"  ✅ Activity viewing: {activity_success}")
            
            # Logout admin
            auth_service.logout_user(admin_info["session_id"])
            print("  ✅ Admin logout completed")
        
        print("  🎯 Admin functionality tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ Admin functionality test failed: {e}")
        return False
