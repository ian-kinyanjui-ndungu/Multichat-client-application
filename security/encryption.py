"""
Advanced encryption module for secure communication.
Implements AES encryption with secure key management.
"""

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecureEncryption:
    def __init__(self, salt: bytes = None, iterations: int = 100000):
        """
        Initialize encryption with configurable salt and iteration count.
        
        Args:
            salt (bytes, optional): Cryptographic salt
            iterations (int, optional): Key derivation iterations
        """
        self.salt = salt or os.urandom(16)
        self.iterations = iterations
        self.key = self._generate_key()

    def _generate_key(self) -> bytes:
        """
        Generate a secure encryption key using PBKDF2.
        
        Returns:
            bytes: Derived encryption key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=self.iterations
        )
        return base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))

    def encrypt(self, message: str) -> str:
        """
        Encrypt a message using Fernet symmetric encryption.
        
        Args:
            message (str): Plain-text message
        
        Returns:
            str: Base64 encoded encrypted message
        """
        f = Fernet(self.key)
        return f.encrypt(message.encode()).decode()

    def decrypt(self, encrypted_message: str) -> str:
        """
        Decrypt a Fernet encrypted message.
        
        Args:
            encrypted_message (str): Base64 encoded encrypted message
        
        Returns:
            str: Decrypted plain-text message
        """
        f = Fernet(self.key)
        return f.decrypt(encrypted_message.encode()).decode()