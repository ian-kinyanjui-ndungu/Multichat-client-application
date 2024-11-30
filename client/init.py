"""
Initialization module for the client package.
Imports and sets up client-related modules and configurations.
"""

from .client import ChatClient
from .gui import ChatGUI

__all__ = ['ChatClient', 'ChatGUI']