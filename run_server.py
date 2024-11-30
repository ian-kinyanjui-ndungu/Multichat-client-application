#!/usr/bin/env python3
"""
Main entry point for running the distributed chat server.
This script initializes and starts the chat server application.
"""

import os
from dotenv import load_dotenv
from server.server import ChatServer

def main():
    # Load environment variables
    load_dotenv()

    # Get server configuration from environment
    host = os.getenv('SERVER_HOST', '127.0.0.1')
    port = int(os.getenv('SERVER_PORT', 5000))
    debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

    # Initialize and start the chat server
    chat_server = ChatServer(host=host, port=port, debug=debug_mode)
    chat_server.start()

if __name__ == '__main__':
    main()