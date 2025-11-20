"""
Image Processing Utilities Module

This module provides utility functions for image processing tasks
including conversion, encoding, and basic manipulations.

Each function has a single responsibility following SOLID principles.

Usage:
    from utils.image_helpers import image_to_base64, base64_to_image
    
    base64_str = image_to_base64(pil_image)
    pil_image = base64_to_image(base64_str)
"""

import base64
from io import BytesIO
from typing import Union
from PIL import Image


def image_to_base64(image: Image.Image, format: str = 'PNG') -> str:
    """
    Convert PIL Image to base64 string.
    
    Responsibility: ONLY convert PIL Image to base64 encoding
    
    Args:
        image (Image.Image): PIL Image object
        format (str): Output format (PNG, JPEG, etc.)
    
    Returns:
        str: Base64 encoded image string
    
    Example:
        >>> img = Image.new('RGB', (100, 100))
        >>> b64 = image_to_base64(img)
        >>> print(b64[:20])  # Shows start of base64 string
    """
    # Create byte buffer to hold image data
    buffer = BytesIO()
    
    # Save image to buffer in specified format
    # This converts PIL Image to bytes
    image.save(buffer, format=format)
    
    # Get byte value from buffer
    image_bytes = buffer.getvalue()
    
    # Encode bytes to base64 string
    # This makes it safe for JSON transmission
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    
    return base64_string


def base64_to_image(base64_string: str) -> Image.Image:
    """
    Convert base64 string to PIL Image.
    
    Responsibility: ONLY convert base64 string to PIL Image
    
    Args:
        base64_string (str): Base64 encoded image string
    
    Returns:
        Image.Image: PIL Image object
    
    Raises:
        ValueError: If base64 string is invalid
    
    Example:
        >>> b64 = "iVBORw0KGgoAAAANS..."
        >>> img = base64_to_image(b64)
        >>> print(img.size)
        (768, 768)
    """
    try:
        # Decode base64 string to bytes
        image_bytes = base64.b64decode(base64_string)
        
        # Create byte buffer from decoded bytes
        buffer = BytesIO(image_bytes)
        
        # Open image from buffer
        image = Image.open(buffer)
        
        return image
    
    except Exception as e:
        raise ValueError(f"Invalid base64 image data: {str(e)}")


def resize_image(
    image: Image.Image,
    width: int,
    height: int,
    maintain_aspect: bool = False
) -> Image.Image:
    """
    Resize image to specified dimensions.
    
    Responsibility: ONLY resize image
    
    Args:
        image (Image.Image): PIL Image to resize
        width (int): Target width
        height (int): Target height
        maintain_aspect (bool): Whether to maintain aspect ratio
    
    Returns:
        Image.Image: Resized image
    
    Note:
        If maintain_aspect is True, image will fit within dimensions
        while preserving original aspect ratio.
    """
    if maintain_aspect:
        # Calculate aspect ratio preserving dimensions
        image.thumbnail((width, height), Image.Resampling.LANCZOS)
        return image
    else:
        # Resize to exact dimensions (may distort)
        return image.resize((width, height), Image.Resampling.LANCZOS)


def get_image_info(image: Image.Image) -> dict:
    """
    Extract image metadata and information.
    
    Responsibility: ONLY extract image properties
    
    Args:
        image (Image.Image): PIL Image object
    
    Returns:
        dict: Image information (size, format, mode, etc.)
    
    Example:
        >>> img = Image.new('RGB', (768, 768))
        >>> info = get_image_info(img)
        >>> print(info['width'])
        768
    """
    return {
        'width': image.width,
        'height': image.height,
        'format': image.format if image.format else 'Unknown',
        'mode': image.mode,
        'size_bytes': len(image.tobytes())
    }


def create_thumbnail(
    image: Image.Image,
    max_size: int = 200
) -> Image.Image:
    """
    Create thumbnail version of image.
    
    Responsibility: ONLY create thumbnail
    
    Args:
        image (Image.Image): Original image
        max_size (int): Maximum dimension for thumbnail
    
    Returns:
        Image.Image: Thumbnail image
    
    Note:
        Maintains aspect ratio, fits within max_size x max_size
    """
    # Create copy to avoid modifying original
    thumbnail = image.copy()
    
    # Create thumbnail (modifies in place)
    thumbnail.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    
    return thumbnail


def ensure_rgb_mode(image: Image.Image) -> Image.Image:
    """
    Ensure image is in RGB mode.
    
    Responsibility: ONLY convert image mode to RGB
    
    Args:
        image (Image.Image): Input image
    
    Returns:
        Image.Image: Image in RGB mode
    
    Note:
        Some models require RGB mode. This converts RGBA, L, etc. to RGB
    """
    if image.mode != 'RGB':
        # Convert to RGB mode
        # RGBA: discards alpha channel
        # L (grayscale): converts to 3-channel RGB
        return image.convert('RGB')
    return image


def calculate_file_size_mb(image: Image.Image, format: str = 'PNG') -> float:
    """
    Calculate approximate file size in megabytes.
    
    Responsibility: ONLY calculate file size
    
    Args:
        image (Image.Image): PIL Image object
        format (str): Output format for size calculation
    
    Returns:
        float: Approximate file size in MB
    
    Example:
        >>> img = Image.new('RGB', (1024, 1024))
        >>> size = calculate_file_size_mb(img)
        >>> print(f"{size:.2f} MB")
    """
    # Create temporary buffer
    buffer = BytesIO()
    
    # Save to buffer to get actual size
    image.save(buffer, format=format)
    
    # Get size in bytes
    size_bytes = len(buffer.getvalue())
    
    # Convert to megabytes
    size_mb = size_bytes / (1024 * 1024)
    
    return size_mb


def pad_to_multiple_of_8(width: int, height: int) -> tuple[int, int]:
    """
    Pad dimensions to nearest multiple of 8.
    
    Responsibility: ONLY calculate padded dimensions
    
    Args:
        width (int): Original width
        height (int): Original height
    
    Returns:
        tuple[int, int]: Padded (width, height)
    
    Note:
        Most diffusion models require dimensions divisible by 8
    
    Example:
        >>> pad_to_multiple_of_8(765, 770)
        (768, 776)
    """
    # Round up to nearest multiple of 8
    padded_width = ((width + 7) // 8) * 8
    padded_height = ((height + 7) // 8) * 8
    
    return padded_width, padded_height


def image_data_url(image: Image.Image, format: str = 'PNG') -> str:
    """
    Convert image to data URL for HTML embedding.
    
    Responsibility: ONLY create data URL
    
    Args:
        image (Image.Image): PIL Image object
        format (str): Image format (PNG, JPEG, etc.)
    
    Returns:
        str: Data URL string (data:image/png;base64,...)
    
    Example:
        >>> img = Image.new('RGB', (100, 100))
        >>> url = image_data_url(img)
        >>> print(url[:30])
        data:image/png;base64,iVBORw0
    """
    # Get base64 encoding
    base64_str = image_to_base64(image, format)
    
    # Determine MIME type from format
    mime_type = f"image/{format.lower()}"
    
    # Create data URL
    data_url = f"data:{mime_type};base64,{base64_str}"
    
    return data_url
