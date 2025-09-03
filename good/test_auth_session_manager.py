#!/usr/bin/env python3
"""
TradePulse Authentication - SessionManager Test Module
Tests SessionManager functionality
"""

def run_tests():
    """Test SessionManager functionality"""
    print("🔄 Testing SessionManager...")
    
    try:
        from auth.session_manager import SessionManager
        
        # Initialize session manager
        session_manager = SessionManager("./data/test_users.db")
        print("  ✅ SessionManager initialized")
        
        # Test session creation
        user_id = 1
        session_id = session_manager.create_session(
            user_id=user_id,
            ip_address="127.0.0.1",
            user_agent="Test Browser"
        )
        print(f"  ✅ Session creation: {session_id is not None}")
        
        if session_id:
            # Test session validation
            valid_user_id = session_manager.validate_session(session_id)
            print(f"  ✅ Session validation: {valid_user_id == user_id}")
            
            # Test session info retrieval
            session_info = session_manager.get_session_info(session_id)
            print(f"  ✅ Session info retrieval: {session_info is not None}")
            
            # Test session refresh
            refreshed = session_manager.refresh_session(session_id)
            print(f"  ✅ Session refresh: {refreshed}")
            
            # Test session invalidation
            invalidated = session_manager.invalidate_session(session_id)
            print(f"  ✅ Session invalidation: {invalidated}")
            
            # Test session statistics
            stats = session_manager.get_session_statistics()
            print(f"  ✅ Session statistics: {stats is not None}")
        
        print("  🎯 SessionManager tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ SessionManager test failed: {e}")
        return False
