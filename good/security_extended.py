#!/usr/bin/env python3
"""
TradePulse Security Extended
Extended security functions for JWT, API keys, and advanced security
"""

import jwt
import hmac
import secrets
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class SecurityExtended:
    """Extended security utilities for JWT, API keys, and advanced features"""
    
    # JWT configuration
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRY_HOURS = 24
    
    @staticmethod
    def generate_jwt_token(user_id: int, username: str, role: str, 
                          additional_claims: Dict = None) -> str:
        """Generate a JWT token for user authentication"""
        try:
            payload = {
                'user_id': user_id,
                'username': username,
                'role': role,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=SecurityExtended.JWT_EXPIRY_HOURS)
            }
            
            if additional_claims:
                payload.update(additional_claims)
            
            token = jwt.encode(
                payload,
                SecurityExtended.JWT_SECRET,
                algorithm=SecurityExtended.JWT_ALGORITHM
            )
            
            logger.debug(f"JWT token generated for user {username}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate JWT token: {e}")
            return None
    
    @staticmethod
    def verify_jwt_token(token: str) -> Optional[Dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(
                token,
                SecurityExtended.JWT_SECRET,
                algorithms=[SecurityExtended.JWT_ALGORITHM]
            )
            
            # Check if token is expired
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                if isinstance(exp_timestamp, (int, float)):
                    import time
                    if time.time() > exp_timestamp:
                        logger.warning("JWT token expired")
                        return None
            
            logger.debug(f"JWT token verified for user {payload.get('username', 'unknown')}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to verify JWT token: {e}")
            return None
    
    @staticmethod
    def generate_api_key(length: int = 32) -> str:
        """Generate a secure API key"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash an API key for storage"""
        import hashlib
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate a CSRF token for form protection"""
        return secrets.token_hex(32)
    
    @staticmethod
    def verify_csrf_token(token: str, stored_token: str) -> bool:
        """Verify a CSRF token"""
        return hmac.compare_digest(token, stored_token)
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not input_string:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', '[', ']']
        sanitized = input_string
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    @staticmethod
    def rate_limit_key(identifier: str, action: str) -> str:
        """Generate a rate limiting key"""
        return f"rate_limit:{identifier}:{action}"
    
    @staticmethod
    def is_rate_limited(identifier: str, action: str, max_attempts: int, 
                       window_seconds: int) -> bool:
        """Check if an action is rate limited"""
        # This is a simplified rate limiting check
        # In production, you'd use Redis or similar for distributed rate limiting
        import time
        current_time = int(time.time())
        window_start = current_time - window_seconds
        
        # For now, return False (not rate limited)
        # Implement actual rate limiting logic here
        return False
