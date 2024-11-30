"""
Authentication management module for the distributed chat application.
Handles user registration, login, and credential verification.
"""

import hashlib
import os
from typing import Dict, Optional
import sqlite3
from security.encryption import SecureEncryption

class AuthenticationManager:
    def __init__(self, database_path: str = 'users.db'):
        """
        Initialize authentication manager with database connection.
        
        Args:
            database_path (str): Path to SQLite user database
        """
        self.database_path = database_path
        self.encryption = SecureEncryption()
        self._create_users_table()

    def _create_users_table(self):
        """
        Create users table if it doesn't exist in the database.
        """
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT,
                    salt TEXT
                )
            ''')
            conn.commit()

    def _hash_password(self, password: str, salt: str = None) -> Dict[str, str]:
        """
        Generate secure password hash with salt.
        
        Args:
            password (str): User's plain-text password
            salt (str, optional): Existing salt or generate new
        
        Returns:
            Dict containing salt and password hash
        """
        if salt is None:
            salt = os.urandom(32).hex()
        
        # Use PBKDF2 for secure password hashing
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt.encode('utf-8'), 
            100000
        ).hex()
        
        return {
            'salt': salt,
            'password_hash': password_hash
        }

    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user in the system.
        
        Args:
            username (str): Chosen username
            password (str): User's password
        
        Returns:
            bool: Registration success status
        """
        try:
            hashed_data = self._hash_password(password)
            
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)',
                    (username, hashed_data['password_hash'], hashed_data['salt'])
                )
                conn.commit()
            
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate user credentials.
        
        Args:
            username (str): User's username
            password (str): User's password
        
        Returns:
            bool: Authentication success status
        """
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT password_hash, salt FROM users WHERE username = ?', 
                (username,)
            )
            result = cursor.fetchone()
            
            if result:
                stored_hash, salt = result
                # Verify password
                verification = self._hash_password(password, salt)
                return verification['password_hash'] == stored_hash
            
            return False