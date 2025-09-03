#!/usr/bin/env python3
"""
TradePulse Authentication - AuthService Test Module
Tests AuthService integration
"""

def run_tests():
    """Test AuthService integration"""
    print("🔐 Testing AuthService...")
    
    try:
        from auth.auth_service import AuthService
        
        # Initialize auth service
        auth_service = AuthService("./data/test_users.db")
        print("  ✅ AuthService initialized")
        
        # Test user registration
        success, message = auth_service.register_user(
            username="testuser2",
            email="test2@example.com",
            password="TestPass123!",
            profile_data={"first_name": "Test2", "last_name": "User2"}
        )
        print(f"  ✅ User registration: {success} - {message}")
        
        if success:
            # Test user authentication
            auth_success, auth_message, user_info = auth_service.authenticate_user(
                username="testuser2",
                password="TestPass123!",
                ip_address="127.0.0.1",
                user_agent="Test Browser"
            )
            print(f"  ✅ User authentication: {auth_success} - {auth_message}")
            
            if auth_success and user_info:
                session_id = user_info.get("session_id")
                
                # Test session validation
                valid, user_data = auth_service.validate_session(session_id)
                print(f"  ✅ Session validation: {valid}")
                
                # Test permission checking
                from auth.rbac import Permission
                has_permission = auth_service.check_permission(
                    user_info["user_id"], 
                    Permission.VIEW_PORTFOLIO
                )
                print(f"  ✅ Permission check: {has_permission}")
                
                # Test logout
                logged_out = auth_service.logout_user(session_id)
                print(f"  ✅ User logout: {logged_out}")
        
        # Test system statistics
        stats = auth_service.get_system_statistics()
        print(f"  ✅ System statistics: {stats is not None}")
        
        print("  🎯 AuthService tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ AuthService test failed: {e}")
        return False
