"""
Comprehensive logging module for the distributed chat application.
Provides flexible and configurable logging capabilities.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logging(
    log_dir: str = 'logs', 
    log_level: str = 'INFO',
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
):
    """
    Configure application-wide logging with file and console handlers.
    
    Args:
        log_dir (str): Directory for log files
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
        log_format (str): Log message format string
    
    Returns:
        logging.Logger: Configured root logger
    """
    # Create logs directory if not exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate unique log filename with timestamp
    log_filename = os.path.join(
        log_dir, 
        f'chat_app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format
    )
    
    # File handler with log rotation
    file_handler = RotatingFileHandler(
        log_filename, 
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Get root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

def get_logger(name: str = 'chat_app') -> logging.Logger:
    """
    Create a named logger for specific components.
    
    Args:
        name (str): Logger name, defaults to 'chat_app'
    
    Returns:
        logging.Logger: Configured named logger
    """
    return logging.getLogger(name)