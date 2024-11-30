"""
Core client-side communication module for the distributed chat application.
Handles socket connections, message transmission, and client-server interactions.
"""

import socket
import threading
import json
from security.encryption import SecureEncryption

class ChatClient:
    def __init__(self, host='localhost', port=5000):
        """
        Initialize the chat client with server connection details.
        
        Args:
            host (str): Server hostname or IP address
            port (int): Server port number
        """
        self.host = host
        self.port = port
        self.socket = None
        self.encryption = SecureEncryption()
        self.is_connected = False

    def connect(self):
        """
        Establish a secure connection with the chat server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            
            # Start listening thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
        except Exception as e:
            print(f"Connection error: {e}")
            self.is_connected = False

    def send_message(self, message, username):
        """
        Send an encrypted message to the server.
        
        Args:
            message (str): Message content
            username (str): Sender's username
        """
        if not self.is_connected:
            return

        encrypted_msg = self.encryption.encrypt(json.dumps({
            'username': username,
            'message': message
        }))
        
        try:
            self.socket.send(encrypted_msg.encode('utf-8'))
        except Exception as e:
            print(f"Send error: {e}")

    def receive_messages(self):
        """
        Continuously listen for incoming messages from the server.
        Decrypts and processes received messages.
        """
        while self.is_connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    decrypted_msg = self.encryption.decrypt(data)
                    message_data = json.loads(decrypted_msg)
                    print(f"{message_data['username']}: {message_data['message']}")
            except Exception as e:
                print(f"Receive error: {e}")
                self.is_connected = False
                break

    def disconnect(self):
        """
        Gracefully close the client socket connection.
        """
        if self.socket:
            self.socket.close()
        self.is_connected = False