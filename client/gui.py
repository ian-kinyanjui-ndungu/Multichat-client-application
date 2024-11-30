"""
Graphical User Interface module for the chat application.
Provides a tkinter-based interactive chat window.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from client import ChatClient

class ChatGUI:
    def __init__(self, client):
        """
        Initialize the chat GUI with a client instance.
        
        Args:
            client (ChatClient): Connected chat client
        """
        self.client = client
        self.root = tk.Tk()
        self.root.title("Distributed Chat Application")
        
        # Chat display area
        self.chat_display = tk.Text(self.root, height=20, width=50)
        self.chat_display.pack(padx=10, pady=10)
        
        # Message input area
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=10)
        
        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10)
        
        # Username
        self.username = self.prompt_username()

    def prompt_username(self):
        """
        Prompt user to enter their username.
        
        Returns:
            str: Entered username
        """
        username = simpledialog.askstring("Username", "Enter your username:")
        return username if username else "Anonymous"

    def send_message(self):
        """
        Send message through the client and update display.
        """
        message = self.message_entry.get()
        if message:
            self.client.send_message(message, self.username)
            self.message_entry.delete(0, tk.END)

    def run(self):
        """
        Start the GUI event loop.
        """
        self.root.mainloop()