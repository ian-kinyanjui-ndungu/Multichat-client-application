import socket
import threading
import json
import logging
from typing import List, Dict, Optional
from security.encryption import SecureEncryption
from .authentication import AuthenticationManager
from .database import DatabaseManager

class ChatServer:
    def __init__(
        self, 
        host: str = '0.0.0.0', 
        port: int = 5000, 
        max_connections: int = 100,
        debug: bool = False  # Add debug parameter
    ):
        """
        Initialize the chat server with network and system configurations.
        
        Args:
            host (str): Server binding address
            port (int): Server listening port
            max_connections (int): Maximum simultaneous client connections
            debug (bool): Enable debug logging
        """
        self.host = host
        self.port = port
        self.max_connections = max_connections
        
        # Configure logging based on debug mode
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Security and management components
        self.encryption = SecureEncryption()
        self.auth_manager = AuthenticationManager()
        self.database_manager = DatabaseManager()
        
        # Client tracking
        self.clients: Dict[str, socket.socket] = {}
        self.client_locks: List[threading.Lock] = [
            threading.Lock() for _ in range(max_connections)
        ]

    def start(self):
        """
        Start the chat server and begin listening for client connections.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_connections)
        
        self.logger.info(f"[*] Server listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                self.logger.debug(f"New connection from {address}")
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_thread.start()
        except KeyboardInterrupt:
            self.logger.info("[!] Server shutting down...")
        finally:
            server_socket.close()

    def handle_client(self, client_socket: socket.socket, address: tuple):
        """
        Handle individual client connections and message processing.
        
        Args:
            client_socket (socket): Connected client socket
            address (tuple): Client network address
        """
        username = None  # Initialize username 
        try:
            # Authentication process
            username = self._authenticate_client(client_socket)
            if not username:
                client_socket.close()
                return

            # Add client to active connections
            with self.client_locks[len(self.clients) % self.max_connections]:
                self.clients[username] = client_socket
            
            self.logger.info(f"User {username} authenticated and connected")

            # Message handling loop
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Decrypt and process message
                decrypted_message = self.encryption.decrypt(data)
                self.logger.debug(f"Received message from {username}: {decrypted_message}")
                self._broadcast_message(username, decrypted_message)

        except Exception as e:
            self.logger.error(f"[!] Client handling error for {username}: {e}")
        finally:
            # Cleanup
            if username and username in self.clients:
                del self.clients[username]
                self.logger.info(f"User {username} disconnected")
            client_socket.close()

    def _authenticate_client(self, client_socket: socket.socket) -> Optional[str]:
        """
        Authenticate incoming client connection.
        
        Args:
            client_socket (socket): Client connection socket
        
        Returns:
            Optional username if authentication successful
        """
        try:
            # Send authentication request
            client_socket.send("AUTH_REQUEST".encode('utf-8'))
            
            # Receive credentials
            credentials = client_socket.recv(1024).decode('utf-8')
            username, password = credentials.split(':')
            
            # Verify credentials
            if self.auth_manager.authenticate_user(username, password):
                client_socket.send("AUTH_SUCCESS".encode('utf-8'))
                self.logger.info(f"Authentication successful for user {username}")
                return username
            
            client_socket.send("AUTH_FAILED".encode('utf-8'))
            self.logger.warning(f"Authentication failed for user {username}")
            return None
        
        except Exception as e:
            self.logger.error(f"[!] Authentication error: {e}")
            return None

    def _broadcast_message(self, sender: str, message: str):
        """
        Broadcast message to all connected clients.
        
        Args:
            sender (str): Message sender's username
            message (str): Encrypted message content
        """
        # Store message in database
        self.database_manager.store_message(sender, message)
        
        # Encrypt and send to all clients
        for username, client_socket in self.clients.items():
            if username != sender:
                encrypted_msg = self.encryption.encrypt(
                    json.dumps({
                        'sender': sender,
                        'message': message
                    })
                )
                client_socket.send(encrypted_msg.encode('utf-8'))
                self.logger.debug(f"Broadcasted message from {sender} to {username}")