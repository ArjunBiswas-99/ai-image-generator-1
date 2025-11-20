"""
Configuration Module

This module manages all application configuration including:
- Environment variables (API keys, secrets)
- Application settings (host, port, debug mode)
- Model defaults (image size, generation parameters)

The Config class provides a centralized location for all settings,
making it easy to modify behavior without changing code throughout
the application.

Usage:
    from config import Config
    config = Config()
    api_key = config.HF_TOKEN
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """
    Application configuration class.
    
    Loads configuration from environment variables and provides
    sensible defaults for all settings. Uses python-dotenv to
    load variables from a .env file if present.
    
    Attributes:
        HF_TOKEN (str): Hugging Face API token for authentication
        HOST (str): Server host address
        PORT (int): Server port number
        DEBUG (bool): Debug mode flag
        DEFAULT_MODEL (str): Default image generation model
        MAX_PROMPT_LENGTH (int): Maximum allowed prompt length
        DEFAULT_WIDTH (int): Default image width in pixels
        DEFAULT_HEIGHT (int): Default image height in pixels
    """
    
    def __init__(self):
        """
        Initialize configuration by loading environment variables.
        
        Automatically loads variables from .env file if it exists,
        then sets all configuration attributes with defaults.
        """
        # Load environment variables from .env file
        # This allows local development without exposing secrets
        load_dotenv()
        
        # API Configuration
        self.HF_TOKEN = self._get_required_env('HF_TOKEN')
        
        # Server Configuration
        self.HOST = self._get_env('HOST', '0.0.0.0')
        self.PORT = self._get_env_int('PORT', 5000)
        self.DEBUG = self._get_env_bool('DEBUG', True)
        
        # Model Configuration
        self.DEFAULT_MODEL = self._get_env(
            'DEFAULT_MODEL',
            'black-forest-labs/FLUX.1-dev'
        )
        
        # Generation Limits
        # These prevent abuse and ensure reasonable resource usage
        self.MAX_PROMPT_LENGTH = 1000
        self.MAX_NEGATIVE_PROMPT_LENGTH = 500
        self.MIN_IMAGE_SIZE = 256
        self.MAX_IMAGE_SIZE = 2048
        
        # Default Generation Parameters
        # These provide good starting values for most use cases
        self.DEFAULT_WIDTH = 768
        self.DEFAULT_HEIGHT = 768
        self.DEFAULT_STEPS = 30
        self.DEFAULT_GUIDANCE_SCALE = 7.5
    
    def _get_env(self, key: str, default: str = '') -> str:
        """
        Get string environment variable with optional default.
        
        Responsibility: ONLY retrieve and return string env var
        
        Args:
            key (str): Environment variable name
            default (str): Default value if not found
        
        Returns:
            str: Environment variable value or default
        """
        return os.getenv(key, default)
    
    def _get_env_int(self, key: str, default: int) -> int:
        """
        Get integer environment variable with default.
        
        Responsibility: ONLY retrieve and convert env var to int
        
        Args:
            key (str): Environment variable name
            default (int): Default value if not found or invalid
        
        Returns:
            int: Environment variable as integer or default
        """
        try:
            return int(os.getenv(key, default))
        except (ValueError, TypeError):
            # If conversion fails, return default
            # This prevents crashes from malformed .env files
            return default
    
    def _get_env_bool(self, key: str, default: bool) -> bool:
        """
        Get boolean environment variable with default.
        
        Responsibility: ONLY retrieve and convert env var to bool
        
        Args:
            key (str): Environment variable name
            default (bool): Default value if not found
        
        Returns:
            bool: Environment variable as boolean or default
            
        Note:
            Accepts 'true', '1', 'yes' as True (case-insensitive)
            Everything else is considered False
        """
        value = os.getenv(key, '').lower()
        if value in ('true', '1', 'yes'):
            return True
        elif value in ('false', '0', 'no'):
            return False
        return default
    
    def _get_required_env(self, key: str) -> str:
        """
        Get required environment variable or raise error.
        
        Responsibility: ONLY retrieve required env var with validation
        
        Args:
            key (str): Environment variable name
        
        Returns:
            str: Environment variable value
        
        Raises:
            ValueError: If environment variable is not set
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(
                f"Required environment variable '{key}' is not set. "
                f"Please create a .env file with {key}=your_value"
            )
        return value
    
    def validate(self) -> bool:
        """
        Validate all configuration settings.
        
        Responsibility: ONLY verify config values are valid
        
        Returns:
            bool: True if all settings are valid
        
        Raises:
            ValueError: If any setting is invalid
        """
        # Validate HF token format (should start with 'hf_')
        if not self.HF_TOKEN.startswith('hf_'):
            raise ValueError(
                "Invalid HuggingFace token format. "
                "Token should start with 'hf_'"
            )
        
        # Validate image size limits make sense
        if self.MIN_IMAGE_SIZE >= self.MAX_IMAGE_SIZE:
            raise ValueError(
                "MIN_IMAGE_SIZE must be less than MAX_IMAGE_SIZE"
            )
        
        # Validate port number is in valid range
        if not (1024 <= self.PORT <= 65535):
            raise ValueError(
                f"Port {self.PORT} is outside valid range (1024-65535)"
            )
        
        return True


# Create a global config instance for easy importing
# This follows the Singleton pattern - one config for the whole app
config = Config()
