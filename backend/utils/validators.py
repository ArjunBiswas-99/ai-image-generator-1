"""
Validation Utilities Module

This module provides validation functions for user inputs.
Each function has a single responsibility: validating one type of input.

The validators ensure data integrity before it reaches the API,
providing clear error messages for debugging and user feedback.

Usage:
    from utils.validators import validate_prompt, validate_image_dimensions
    
    validate_prompt("A beautiful sunset")
    validate_image_dimensions(768, 768)
"""

from typing import Optional


def validate_prompt(prompt: str, max_length: int = 1000) -> bool:
    """
    Validate text prompt for image generation.
    
    Responsibility: ONLY check prompt validity
    
    Args:
        prompt (str): User's text prompt
        max_length (int): Maximum allowed prompt length
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If prompt is invalid with specific reason
    
    Example:
        >>> validate_prompt("A red car")
        True
        >>> validate_prompt("")
        ValueError: Prompt cannot be empty
    """
    # Check if prompt exists
    if not prompt:
        raise ValueError("Prompt cannot be empty")
    
    # Check if prompt has content after stripping whitespace
    if not prompt.strip():
        raise ValueError("Prompt cannot be only whitespace")
    
    # Check prompt length
    if len(prompt) > max_length:
        raise ValueError(
            f"Prompt too long: {len(prompt)} characters "
            f"(maximum: {max_length})"
        )
    
    return True


def validate_negative_prompt(
    negative_prompt: Optional[str],
    max_length: int = 500
) -> bool:
    """
    Validate negative prompt (optional field).
    
    Responsibility: ONLY check negative prompt validity
    
    Args:
        negative_prompt (Optional[str]): User's negative prompt
        max_length (int): Maximum allowed length
    
    Returns:
        bool: True if valid or None
    
    Raises:
        ValueError: If negative prompt is invalid
    
    Note:
        None or empty string is considered valid (optional field)
    """
    # Negative prompt is optional, so None/empty is valid
    if not negative_prompt:
        return True
    
    # If provided, check length
    if len(negative_prompt) > max_length:
        raise ValueError(
            f"Negative prompt too long: {len(negative_prompt)} characters "
            f"(maximum: {max_length})"
        )
    
    return True


def validate_image_dimensions(
    width: int,
    height: int,
    min_size: int = 256,
    max_size: int = 2048
) -> bool:
    """
    Validate image width and height.
    
    Responsibility: ONLY check dimension validity
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
        min_size (int): Minimum allowed dimension
        max_size (int): Maximum allowed dimension
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If dimensions are invalid
        TypeError: If dimensions are not integers
    
    Example:
        >>> validate_image_dimensions(768, 768)
        True
        >>> validate_image_dimensions(100, 100)
        ValueError: Width 100 is below minimum (256)
    """
    # Check types
    if not isinstance(width, int):
        raise TypeError(f"Width must be integer, got {type(width).__name__}")
    
    if not isinstance(height, int):
        raise TypeError(f"Height must be integer, got {type(height).__name__}")
    
    # Check minimum dimensions
    if width < min_size:
        raise ValueError(f"Width {width} is below minimum ({min_size})")
    
    if height < min_size:
        raise ValueError(f"Height {height} is below minimum ({min_size})")
    
    # Check maximum dimensions
    if width > max_size:
        raise ValueError(f"Width {width} exceeds maximum ({max_size})")
    
    if height > max_size:
        raise ValueError(f"Height {height} exceeds maximum ({max_size})")
    
    # Check if dimensions are multiples of 8
    # Most diffusion models require this
    if width % 8 != 0:
        raise ValueError(f"Width {width} must be multiple of 8")
    
    if height % 8 != 0:
        raise ValueError(f"Height {height} must be multiple of 8")
    
    return True


def validate_steps(
    steps: int,
    min_steps: int = 1,
    max_steps: int = 100
) -> bool:
    """
    Validate number of inference steps.
    
    Responsibility: ONLY check steps validity
    
    Args:
        steps (int): Number of inference steps
        min_steps (int): Minimum allowed steps
        max_steps (int): Maximum allowed steps
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If steps are invalid
        TypeError: If steps is not an integer
    """
    # Check type
    if not isinstance(steps, int):
        raise TypeError(f"Steps must be integer, got {type(steps).__name__}")
    
    # Check range
    if steps < min_steps:
        raise ValueError(
            f"Steps {steps} is below minimum ({min_steps})"
        )
    
    if steps > max_steps:
        raise ValueError(
            f"Steps {steps} exceeds maximum ({max_steps})"
        )
    
    return True


def validate_guidance_scale(
    guidance: float,
    min_guidance: float = 1.0,
    max_guidance: float = 20.0
) -> bool:
    """
    Validate guidance scale value.
    
    Responsibility: ONLY check guidance scale validity
    
    Args:
        guidance (float): Guidance scale value
        min_guidance (float): Minimum allowed value
        max_guidance (float): Maximum allowed value
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If guidance is invalid
        TypeError: If guidance is not a number
    
    Note:
        Guidance scale controls how closely the model follows the prompt.
        Typical range is 1.0 to 20.0, with 7.5 being common default.
    """
    # Check type (allow int or float)
    if not isinstance(guidance, (int, float)):
        raise TypeError(
            f"Guidance must be numeric, got {type(guidance).__name__}"
        )
    
    # Convert to float for comparison
    guidance = float(guidance)
    
    # Check range
    if guidance < min_guidance:
        raise ValueError(
            f"Guidance {guidance} is below minimum ({min_guidance})"
        )
    
    if guidance > max_guidance:
        raise ValueError(
            f"Guidance {guidance} exceeds maximum ({max_guidance})"
        )
    
    return True


def validate_seed(seed: Optional[int]) -> bool:
    """
    Validate random seed value.
    
    Responsibility: ONLY check seed validity
    
    Args:
        seed (Optional[int]): Random seed for reproducibility
    
    Returns:
        bool: True if valid or None
    
    Raises:
        ValueError: If seed is invalid
        TypeError: If seed is not an integer
    
    Note:
        Seed is optional. None means random generation.
        Valid seeds are typically 0 to 2^32-1
    """
    # Seed is optional
    if seed is None:
        return True
    
    # Check type
    if not isinstance(seed, int):
        raise TypeError(f"Seed must be integer, got {type(seed).__name__}")
    
    # Check range (32-bit unsigned integer)
    if seed < 0:
        raise ValueError("Seed cannot be negative")
    
    if seed > 2**32 - 1:
        raise ValueError(
            f"Seed {seed} too large (maximum: {2**32 - 1})"
        )
    
    return True


def validate_model_id(model_id: str, valid_models: list) -> bool:
    """
    Validate model identifier against list of valid models.
    
    Responsibility: ONLY check if model ID is in valid list
    
    Args:
        model_id (str): Model identifier to validate
        valid_models (list): List of valid model IDs
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If model ID is invalid
    
    Example:
        >>> validate_model_id('FLUX.1-dev', ['FLUX.1-dev', 'SDXL'])
        True
    """
    if not model_id:
        raise ValueError("Model ID cannot be empty")
    
    if model_id not in valid_models:
        raise ValueError(
            f"Invalid model ID: '{model_id}'. "
            f"Must be one of: {', '.join(valid_models)}"
        )
    
    return True
