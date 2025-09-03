#!/usr/bin/env python3
"""
TradePulse Authentication - SecurityUtils Test Module
Tests SecurityUtils functionality
"""

def run_tests():
    """Test SecurityUtils functionality"""
    print("🔐 Testing SecurityUtils...")
    
    try:
        from auth.security_utils import SecurityUtils
        
        # Test password hashing
        password = "TestPassword123!"
        hashed = SecurityUtils.hash_password(password)
        print(f"  ✅ Password hashing: {len(hashed)} characters")
        
        # Test password verification
        is_valid = SecurityUtils.verify_password(password, hashed)
        print(f"  ✅ Password verification: {is_valid}")
        
        # Test password strength validation
        weak_password = "weak"
        is_strong, message = SecurityUtils.validate_password_strength(weak_password)
        print(f"  ✅ Password strength validation: {is_strong} - {message}")
        
        # Test JWT token generation
        token = SecurityUtils.generate_jwt_token(1, "testuser", "user")
        print(f"  ✅ JWT token generation: {len(token)} characters")
        
        # Test JWT token verification
        payload = SecurityUtils.verify_jwt_token(token)
        print(f"  ✅ JWT token verification: {payload is not None}")
        
        # Test data encryption/decryption
        test_data = "sensitive information"
        encrypted = SecurityUtils.encrypt_data(test_data)
        decrypted = SecurityUtils.decrypt_data(encrypted)
        print(f"  ✅ Data encryption/decryption: {test_data == decrypted}")
        
        print("  🎯 SecurityUtils tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ SecurityUtils test failed: {e}")
        return False
