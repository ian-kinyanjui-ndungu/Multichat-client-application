"""
Database management module for the distributed chat application.
Handles message storage, retrieval, and database operations.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, database_path: str = 'chat_database.db'):
        """
        Initialize database manager with connection setup.
        
        Args:
            database_path (str): Path to SQLite chat database
        """
        self.database_path = database_path
        self._create_tables()

    def _create_tables(self):
        """
        Create necessary tables for chat application.
        """
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    room TEXT
                )
            ''')
            
            # Users table (if not created by AuthenticationManager)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    last_seen DATETIME
                )
            ''')
            
            conn.commit()

    def store_message(self, sender: str, content: str, room: str = 'global') -> int:
        """
        Store a chat message in the database.
        
        Args:
            sender (str): Message sender's username
            content (str): Message content
            room (str, optional): Chat room/channel
        
        Returns:
            int: Stored message ID
        """
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (sender, content, room) VALUES (?, ?, ?)',
                (sender, content, room)
            )
            conn.commit()
            return cursor.lastrowid

    def get_recent_messages(
        self, 
        limit: int = 50, 
        room: str = 'global'
    ) -> List[Dict[str, str]]:
        """
        Retrieve recent messages from the database.
        
        Args:
            limit (int, optional): Number of recent messages
            room (str, optional): Specific chat room
        
        Returns:
            List of message dictionaries
        """
        with sqlite3.connect(self.database_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                '''SELECT * FROM messages 
                   WHERE room = ? 
                   ORDER BY timestamp DESC 
                   LIMIT ?''', 
                (room, limit)
            )
            
            return [dict(row) for row in cursor.fetchall()]

    def update_user_last_seen(self, username: str) -> None:
        """
        Update user's last seen timestamp.
        
        Args:
            username (str): User's username
        """
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT OR REPLACE INTO users (username, last_seen) 
                   VALUES (?, CURRENT_TIMESTAMP)''', 
                (username,)
            )
            conn.commit()