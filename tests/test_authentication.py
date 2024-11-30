"""
Unit tests for the authentication module.
Validates user registration and authentication processes.
"""

import unittest
import sys
import os
import tempfile

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.authentication import AuthenticationManager

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        """
        Create a temporary database for testing.
        """
        self.temp_db = tempfile.mktemp()
        self.auth_manager = AuthenticationManager(database_path=self.temp_db)

    def test_user_registration(self):
        """
        Test successful user registration.
        """
        result = self.auth_manager.register_user('testuser', 'password123')
        self.assertTrue(result, "User registration should succeed")

    def test_duplicate_registration(self):
        """
        Test prevention of duplicate username registration.
        """
        self.auth_manager.register_user('uniqueuser', 'password123')
        result = self.auth_manager.register_user('uniqueuser', 'different_password')
        self.assertFalse(result, "Duplicate username registration should fail")

    def test_successful_authentication(self):
        """
        Test successful user authentication.
        """
        username = 'authuser'
        password = 'correct_password'
        
        self.auth_manager.register_user(username, password)
        auth_result = self.auth_manager.authenticate_user(username, password)
        
        self.assertTrue(auth_result, "Correct credentials should authenticate")

    def test_failed_authentication(self):
        """
        Test authentication failure with incorrect credentials.
        """
        username = 'failuser'
        correct_password = 'correct_password'
        wrong_password = 'wrong_password'
        
        self.auth_manager.register_user(username, correct_password)
        auth_result = self.auth_manager.authenticate_user(username, wrong_password)
        
        self.assertFalse(auth_result, "Incorrect password should fail authentication")

    def tearDown(self):
        """
        Clean up temporary database after tests.
        """
        if os.path.exists(self.temp_db):
            os.unlink(self.temp_db)

if __name__ == '__main__':
    unittest.main()