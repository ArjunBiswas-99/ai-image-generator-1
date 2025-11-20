"""
Image Generation Service Module

This module handles all communication with the Hugging Face API
for text-to-image generation. It provides a clean interface that
abstracts away API complexity.

Follows Single Responsibility Principle - only handles image generation
via HuggingFace, nothing else.

Usage:
    from services.image_service import ImageGenerationService
    
    service = ImageGenerationService(api_key="hf_...")
    result = service.generate_image("A sunset", "FLUX.1-dev")
"""

import logging
from datetime import datetime
from typing import Dict, Optional
from PIL import Image
from huggingface_hub import InferenceClient

from utils.image_helpers import image_to_base64, get_image_info
from utils.validators import validate_prompt, validate_negative_prompt


# Configure logging for this module
logger = logging.getLogger(__name__)


class ImageGenerationService:
    """
    Service for generating images via Hugging Face API.
    
    This class encapsulates all image generation logic, managing
    API authentication, request formatting, and response handling.
    
    Attributes:
        client (InferenceClient): Authenticated HuggingFace client
        api_key (str): API key for authentication
    
    Example:
        service = ImageGenerationService(api_key="hf_...")
        result = service.generate_image(
            prompt="A beautiful sunset",
            model_id="black-forest-labs/FLUX.1-dev",
            width=768,
            height=768
        )
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the image generation service.
        
        Responsibility: ONLY set up API client with authentication
        
        Args:
            api_key (str): HuggingFace API token
        
        Raises:
            ValueError: If api_key is empty or invalid
        """
        if not api_key:
            raise ValueError("API key cannot be empty")
        
        if not api_key.startswith('hf_'):
            logger.warning("API key does not start with 'hf_' - may be invalid")
        
        self.api_key = api_key
        self.client = InferenceClient(api_key=api_key)
        
        logger.info("ImageGenerationService initialized successfully")
    
    def generate_image(
        self,
        prompt: str,
        model_id: str,
        width: int = 768,
        height: int = 768,
        num_inference_steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None
    ) -> Dict:
        """
        Generate a single image from text prompt.
        
        Responsibility: ONLY orchestrate the image generation process
        
        This method:
        1. Validates inputs
        2. Calls HuggingFace API
        3. Processes response
        4. Returns formatted result
        
        Args:
            prompt (str): Text description of desired image
            model_id (str): HuggingFace model identifier
            width (int): Image width in pixels
            height (int): Image height in pixels
            num_inference_steps (Optional[int]): Number of denoising steps
            guidance_scale (Optional[float]): Prompt adherence strength
            negative_prompt (Optional[str]): What to avoid in generation
            seed (Optional[int]): Random seed for reproducibility
        
        Returns:
            Dict: Contains 'success', 'image' (base64), 'metadata'
        
        Raises:
            ValueError: If inputs are invalid
            Exception: If API call fails
        
        Example:
            result = service.generate_image(
                prompt="A red sports car",
                model_id="black-forest-labs/FLUX.1-dev",
                width=768,
                height=768,
                guidance_scale=7.5
            )
        """
        try:
            # Step 1: Validate inputs
            # This ensures bad data never reaches the API
            logger.info(f"Validating generation request for model: {model_id}")
            self._validate_generation_inputs(prompt, negative_prompt)
            
            # Step 2: Build parameters dictionary
            # Only include parameters that are actually set
            params = self._build_generation_params(
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                negative_prompt=negative_prompt,
                seed=seed
            )
            
            # Step 3: Call HuggingFace API
            logger.info(f"Calling HuggingFace API with prompt: '{prompt[:50]}...'")
            image = self._call_api(prompt, model_id, params)
            
            # Step 4: Process and format response
            result = self._format_success_response(image, model_id, prompt, params)
            
            logger.info("Image generated successfully")
            return result
        
        except Exception as e:
            # Handle any errors that occurred
            logger.error(f"Image generation failed: {str(e)}")
            return self._format_error_response(str(e))
    
    def _validate_generation_inputs(
        self,
        prompt: str,
        negative_prompt: Optional[str]
    ) -> None:
        """
        Validate generation inputs before API call.
        
        Responsibility: ONLY validate prompt-related inputs
        
        Args:
            prompt (str): Main prompt to validate
            negative_prompt (Optional[str]): Negative prompt to validate
        
        Raises:
            ValueError: If any input is invalid
        """
        # Validate main prompt
        validate_prompt(prompt)
        
        # Validate negative prompt if provided
        if negative_prompt:
            validate_negative_prompt(negative_prompt)
    
    def _build_generation_params(
        self,
        width: int,
        height: int,
        num_inference_steps: Optional[int],
        guidance_scale: Optional[float],
        negative_prompt: Optional[str],
        seed: Optional[int]
    ) -> Dict:
        """
        Build parameters dictionary for API call.
        
        Responsibility: ONLY construct parameters dict
        
        Args:
            width (int): Image width
            height (int): Image height
            num_inference_steps (Optional[int]): Number of steps
            guidance_scale (Optional[float]): Guidance value
            negative_prompt (Optional[str]): Negative prompt
            seed (Optional[int]): Random seed
        
        Returns:
            Dict: Parameters ready for API call
        
        Note:
            Only includes non-None parameters to avoid API errors
        """
        params = {
            'width': width,
            'height': height
        }
        
        # Only add optional parameters if they are provided
        # This prevents sending None values to the API
        if num_inference_steps is not None:
            params['num_inference_steps'] = num_inference_steps
        
        if guidance_scale is not None:
            params['guidance_scale'] = guidance_scale
        
        if negative_prompt:
            params['negative_prompt'] = negative_prompt
        
        if seed is not None:
            params['seed'] = seed
        
        return params
    
    def _call_api(
        self,
        prompt: str,
        model_id: str,
        params: Dict
    ) -> Image.Image:
        """
        Make API call to HuggingFace.
        
        Responsibility: ONLY communicate with HuggingFace API
        
        Args:
            prompt (str): Text prompt
            model_id (str): Model identifier
            params (Dict): Generation parameters
        
        Returns:
            Image.Image: Generated PIL Image
        
        Raises:
            Exception: If API call fails
        """
        try:
            # Call HuggingFace text_to_image API
            # The client handles authentication automatically
            image = self.client.text_to_image(
                prompt=prompt,
                model=model_id,
                **params
            )
            
            return image
        
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"HuggingFace API call failed: {str(e)}")
    
    def _format_success_response(
        self,
        image: Image.Image,
        model_id: str,
        prompt: str,
        params: Dict
    ) -> Dict:
        """
        Format successful generation response.
        
        Responsibility: ONLY format success response structure
        
        Args:
            image (Image.Image): Generated image
            model_id (str): Model that was used
            prompt (str): Prompt that was used
            params (Dict): Parameters that were used
        
        Returns:
            Dict: Formatted response with image and metadata
        """
        # Convert image to base64 for JSON transmission
        image_base64 = image_to_base64(image)
        
        # Extract image information
        image_info = get_image_info(image)
        
        # Build response
        return {
            'success': True,
            'image': image_base64,
            'metadata': {
                'model_id': model_id,
                'prompt': prompt,
                'width': image_info['width'],
                'height': image_info['height'],
                'parameters': params,
                'timestamp': datetime.now().isoformat()
            }
        }
    
    def _format_error_response(self, error_message: str) -> Dict:
        """
        Format error response.
        
        Responsibility: ONLY format error response structure
        
        Args:
            error_message (str): Error description
        
        Returns:
            Dict: Formatted error response
        """
        return {
            'success': False,
            'error': error_message,
            'timestamp': datetime.now().isoformat()
        }
    
    def test_connection(self) -> bool:
        """
        Test if API connection is working.
        
        Responsibility: ONLY test API connectivity
        
        Returns:
            bool: True if connection works, False otherwise
        
        Example:
            if service.test_connection():
                print("API is ready!")
        """
        try:
            # Try a minimal API call to test connection
            # Using a small, fast model for testing
            test_image = self.client.text_to_image(
                prompt="test",
                model="black-forest-labs/FLUX.1-dev",
                width=256,
                height=256
            )
            logger.info("API connection test successful")
            return True
        
        except Exception as e:
            logger.error(f"API connection test failed: {str(e)}")
            return False
