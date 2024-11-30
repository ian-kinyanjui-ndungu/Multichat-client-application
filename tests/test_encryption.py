"""
Unit tests for the encryption module.
Validates encryption and decryption functionality.
"""

import unittest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from security.encryption import SecureEncryption

class TestSecureEncryption(unittest.TestCase):
    def setUp(self):
        """
        Initialize encryption instance for each test.
        """
        self.encryptor = SecureEncryption()

    def test_encryption_decryption(self):
        """
        Test that a message can be encrypted and then decrypted correctly.
        """
        original_message = "Hello, Secure World!"
        encrypted_message = self.encryptor.encrypt(original_message)
        decrypted_message = self.encryptor.decrypt(encrypted_message)
        
        self.assertEqual(
            original_message, 
            decrypted_message, 
            "Decrypted message does not match original"
        )

    def test_different_messages(self):
        """
        Ensure different messages produce different encrypted outputs.
        """
        message1 = "Test Message 1"
        message2 = "Test Message 2"
        
        encrypted1 = self.encryptor.encrypt(message1)
        encrypted2 = self.encryptor.encrypt(message2)
        
        self.assertNotEqual(
            encrypted1, 
            encrypted2, 
            "Different messages should produce different encryptions"
        )

    def test_encryption_with_special_characters(self):
        """
        Test encryption with messages containing special characters.
        """
        special_message = "Hello, World! @#$%^&* (Test)"
        encrypted_message = self.encryptor.encrypt(special_message)
        decrypted_message = self.encryptor.decrypt(encrypted_message)
        
        self.assertEqual(
            special_message, 
            decrypted_message, 
            "Special character message encryption failed"
        )

if __name__ == '__main__':
    unittest.main()