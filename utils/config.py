"""
Configuration management module for the distributed chat application.
Handles loading and parsing configuration from environment and files.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

def load_configuration(env_path: str = '.env') -> Dict[str, Any]:
    """
    Load configuration from environment variables and .env file.
    
    Args:
        env_path (str): Path to .env configuration file
    
    Returns:
        Dict containing configuration settings
    """
    # Load environment variables from .env file
    load_dotenv(env_path)
    
    # Configuration dictionary to store settings
    config = {
        'SERVER': {
            'HOST': os.getenv('SERVER_HOST', '127.0.0.1'),
            'PORT': int(os.getenv('SERVER_PORT', 5000)),
            'DEBUG': os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        },
        'DATABASE': {
            'URL': os.getenv('DATABASE_URL', 'sqlite:///chat_application.db'),
            'MAX_CONNECTIONS': int(os.getenv('DB_MAX_CONNECTIONS', 5))
        },
        'SECURITY': {
            'SECRET_KEY': os.getenv('SECRET_KEY', 'default_secret_key'),
            'ENCRYPTION_SALT': os.getenv('ENCRYPTION_SALT', 'default_salt'),
            'SSL_CERT_PATH': os.getenv('SSL_CERT_PATH', './security/cert.pem'),
            'SSL_KEY_PATH': os.getenv('SSL_KEY_PATH', './security/key.pem')
        },
        'LOGGING': {
            'LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
            'FILE_PATH': os.getenv('LOG_FILE_PATH', './logs/chat_app.log')
        }
    }
    
    return config

def validate_configuration(config: Dict[str, Any]) -> bool:
    """
    Validate loaded configuration for required settings.
    
    Args:
        config (Dict): Configuration dictionary
    
    Returns:
        bool: Configuration validity status
    """
    required_keys = [
        'SERVER.HOST', 
        'SERVER.PORT', 
        'SECURITY.SECRET_KEY'
    ]
    
    for key in required_keys:
        section, setting = key.split('.')
        if not config.get(section, {}).get(setting):
            print(f"Missing required configuration: {key}")
            return False
    
    return True