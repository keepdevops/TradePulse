#!/usr/bin/env python3
"""
TradePulse Security Core
Core security functions for password hashing and encryption
"""

import hashlib
import hmac
import secrets
import time
import logging
from datetime import datetime, timedelta
from typing import Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

logger = logging.getLogger(__name__)

class SecurityCore:
    """Core security utilities for authentication and encryption"""
    
    # Configuration
    SALT_LENGTH = 32
    HASH_ITERATIONS = 100000
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
    
    @staticmethod
    def generate_salt(length: int = None) -> str:
        """Generate a random salt for password hashing"""
        length = length or SecurityCore.SALT_LENGTH
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> str:
        """Hash a password using PBKDF2 with salt"""
        if salt is None:
            salt = SecurityCore.generate_salt()
        
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt.encode(),
                iterations=SecurityCore.HASH_ITERATIONS,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return f"{salt}:{key.decode()}"
            
        except Exception as e:
            logger.error(f"Failed to hash password: {e}")
            # Fallback to SHA256 if PBKDF2 fails
            return f"{salt}:{hashlib.sha256((password + salt).encode()).hexdigest()}"
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            if ':' not in hashed_password:
                return False
            
            salt, stored_hash = hashed_password.split(':', 1)
            computed_hash = SecurityCore.hash_password(password, salt)
            computed_salt, computed_stored_hash = computed_hash.split(':', 1)
            
            # Use constant-time comparison to prevent timing attacks
            return hmac.compare_digest(stored_hash, computed_stored_hash)
            
        except Exception as e:
            logger.error(f"Failed to verify password: {e}")
            return False
    
    @staticmethod
    def encrypt_data(data: str) -> str:
        """Encrypt sensitive data"""
        try:
            fernet = Fernet(SecurityCore.ENCRYPTION_KEY)
            encrypted_data = fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
            
        except Exception as e:
            logger.error(f"Failed to encrypt data: {e}")
            return data
    
    @staticmethod
    def decrypt_data(encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            fernet = Fernet(SecurityCore.ENCRYPTION_KEY)
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = fernet.decrypt(decoded_data)
            return decrypted_data.decode()
            
        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            return encrypted_data
    
    @staticmethod
    def generate_secure_random_string(length: int = 16) -> str:
        """Generate a cryptographically secure random string"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """Validate password strength requirements"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password must contain at least one special character"
        
        return True, "Password meets strength requirements"
