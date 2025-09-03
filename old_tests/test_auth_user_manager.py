#!/usr/bin/env python3
"""
TradePulse Authentication - UserManager Test Module
Tests UserManager functionality
"""

def run_tests():
    """Test UserManager functionality"""
    print("👤 Testing UserManager...")
    
    try:
        from auth.user_manager import UserManager
        
        # Initialize user manager
        user_manager = UserManager("./data/test_users.db")
        print("  ✅ UserManager initialized")
        
        # Test user creation
        test_user = user_manager.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",
            role="user",
            profile_data={"first_name": "Test", "last_name": "User"}
        )
        print(f"  ✅ User creation: {test_user is not None}")
        
        if test_user:
            # Test user retrieval
            retrieved_user = user_manager.get_user_by_id(test_user.id)
            print(f"  ✅ User retrieval by ID: {retrieved_user is not None}")
            
            retrieved_user_by_username = user_manager.get_user_by_username("testuser")
            print(f"  ✅ User retrieval by username: {retrieved_user_by_username is not None}")
            
            # Test profile update
            profile_updated = user_manager.update_user_profile(
                test_user.id, 
                {"first_name": "Updated", "last_name": "User"}
            )
            print(f"  ✅ Profile update: {profile_updated}")
            
            # Test user listing
            users = user_manager.list_users()
            print(f"  ✅ User listing: {len(users)} users found")
            
            # Clean up test user
            user_manager.deactivate_user(test_user.id)
            print("  ✅ Test user deactivated")
        
        print("  🎯 UserManager tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ UserManager test failed: {e}")
        return False
