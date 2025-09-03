#!/usr/bin/env python3
"""
TradePulse Security Utils
Main security utilities module - imports from security_core and security_extended
"""

from .security_core import SecurityCore
from .security_extended import SecurityExtended

# Re-export all security functions for backward compatibility
class SecurityUtils:
    """Main security utilities class - combines core and extended security features"""
    
    # Core security functions
    generate_salt = SecurityCore.generate_salt
    hash_password = SecurityCore.hash_password
    verify_password = SecurityCore.verify_password
    encrypt_data = SecurityCore.encrypt_data
    decrypt_data = SecurityCore.decrypt_data
    generate_secure_random_string = SecurityCore.generate_secure_random_string
    validate_password_strength = SecurityCore.validate_password_strength
    
    # Extended security functions
    generate_jwt_token = SecurityExtended.generate_jwt_token
    verify_jwt_token = SecurityExtended.verify_jwt_token
    generate_api_key = SecurityExtended.generate_api_key
    hash_api_key = SecurityExtended.hash_api_key
    generate_csrf_token = SecurityExtended.generate_csrf_token
    verify_csrf_token = SecurityExtended.verify_csrf_token
    sanitize_input = SecurityExtended.sanitize_input
    rate_limit_key = SecurityExtended.rate_limit_key
    is_rate_limited = SecurityExtended.is_rate_limited
