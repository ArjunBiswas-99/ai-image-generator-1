"""
Models Configuration Module

This module defines all available image generation models and their
specifications. Each model has metadata about its capabilities,
limitations, and optimal parameters.

The centralized model registry makes it easy to:
- Add new models without changing other code
- Provide model information to the frontend
- Validate parameters against model capabilities
- Document model characteristics

Usage:
    from models.models_config import get_all_models, get_model_by_id
    
    models = get_all_models()
    model_info = get_model_by_id('black-forest-labs/FLUX.1-dev')
"""

from typing import List, Dict, Optional


# Model registry - centralized list of all available models
# Each model has comprehensive metadata for validation and UI display
AVAILABLE_MODELS = [
    {
        'id': 'black-forest-labs/FLUX.1-dev',
        'name': 'FLUX.1 Dev',
        'description': 'High-quality image generation model with excellent prompt following',
        'provider': 'fal-ai',
        'category': 'general',
        'max_width': 2048,
        'max_height': 2048,
        'default_width': 768,
        'default_height': 768,
        'supports_negative_prompt': True,
        'supports_seed': True,
        'min_steps': 20,
        'max_steps': 50,
        'default_steps': 30,
        'min_guidance': 1.0,
        'max_guidance': 20.0,
        'default_guidance': 7.5,
        'estimated_time': '15-30 seconds',
        'tags': ['realistic', 'versatile', 'high-quality']
    },
    {
        'id': 'ByteDance/SDXL-Lightning',
        'name': 'SDXL Lightning',
        'description': 'Fast, high-quality image generation optimized for speed',
        'provider': 'fal-ai',
        'category': 'fast',
        'max_width': 1024,
        'max_height': 1024,
        'default_width': 768,
        'default_height': 768,
        'supports_negative_prompt': True,
        'supports_seed': True,
        'min_steps': 4,
        'max_steps': 20,
        'default_steps': 8,
        'min_guidance': 1.0,
        'max_guidance': 12.0,
        'default_guidance': 7.0,
        'estimated_time': '5-10 seconds',
        'tags': ['fast', 'efficient', 'realistic']
    },
    {
        'id': 'stabilityai/stable-diffusion-xl-base-1.0',
        'name': 'Stable Diffusion XL',
        'description': 'Popular and reliable image generation model',
        'provider': 'replicate',
        'category': 'general',
        'max_width': 1536,
        'max_height': 1536,
        'default_width': 768,
        'default_height': 768,
        'supports_negative_prompt': True,
        'supports_seed': True,
        'min_steps': 20,
        'max_steps': 100,
        'default_steps': 50,
        'min_guidance': 1.0,
        'max_guidance': 20.0,
        'default_guidance': 7.5,
        'estimated_time': '20-40 seconds',
        'tags': ['reliable', 'versatile', 'popular']
    },
    {
        'id': 'ByteDance/Hyper-SD',
        'name': 'Hyper-SD',
        'description': 'Advanced model with excellent detail and coherence',
        'provider': 'fal-ai',
        'category': 'general',
        'max_width': 1024,
        'max_height': 1024,
        'default_width': 768,
        'default_height': 768,
        'supports_negative_prompt': True,
        'supports_seed': True,
        'min_steps': 15,
        'max_steps': 40,
        'default_steps': 25,
        'min_guidance': 1.0,
        'max_guidance': 15.0,
        'default_guidance': 7.5,
        'estimated_time': '10-20 seconds',
        'tags': ['detailed', 'coherent', 'balanced']
    },
    {
        'id': 'Qwen/Qwen-Image',
        'name': 'Qwen Image',
        'description': 'Powerful model with strong artistic capabilities',
        'provider': 'nebius',
        'category': 'artistic',
        'max_width': 2048,
        'max_height': 2048,
        'default_width': 768,
        'default_height': 768,
        'supports_negative_prompt': True,
        'supports_seed': True,
        'min_steps': 20,
        'max_steps': 60,
        'default_steps': 30,
        'min_guidance': 1.0,
        'max_guidance': 20.0,
        'default_guidance': 8.0,
        'estimated_time': '15-30 seconds',
        'tags': ['artistic', 'creative', 'versatile']
    }
]


def get_all_models() -> List[Dict]:
    """
    Get list of all available models.
    
    Responsibility: ONLY return the complete model list
    
    Returns:
        List[Dict]: List of all model configurations
    
    Example:
        >>> models = get_all_models()
        >>> print(f"Found {len(models)} models")
        Found 5 models
    """
    return AVAILABLE_MODELS.copy()


def get_model_by_id(model_id: str) -> Optional[Dict]:
    """
    Get specific model configuration by ID.
    
    Responsibility: ONLY find and return matching model
    
    Args:
        model_id (str): Unique model identifier (e.g., 'black-forest-labs/FLUX.1-dev')
    
    Returns:
        Optional[Dict]: Model configuration if found, None otherwise
    
    Example:
        >>> model = get_model_by_id('black-forest-labs/FLUX.1-dev')
        >>> print(model['name'])
        FLUX.1 Dev
    """
    for model in AVAILABLE_MODELS:
        if model['id'] == model_id:
            return model.copy()
    return None


def get_models_by_category(category: str) -> List[Dict]:
    """
    Get all models in a specific category.
    
    Responsibility: ONLY filter models by category
    
    Args:
        category (str): Category name ('general', 'fast', 'artistic', etc.)
    
    Returns:
        List[Dict]: List of models in the specified category
    
    Example:
        >>> fast_models = get_models_by_category('fast')
        >>> print(f"Found {len(fast_models)} fast models")
        Found 1 fast models
    """
    return [
        model.copy()
        for model in AVAILABLE_MODELS
        if model['category'] == category
    ]


def get_models_by_tag(tag: str) -> List[Dict]:
    """
    Get all models with a specific tag.
    
    Responsibility: ONLY filter models by tag
    
    Args:
        tag (str): Tag name ('realistic', 'fast', 'artistic', etc.)
    
    Returns:
        List[Dict]: List of models with the specified tag
    
    Example:
        >>> realistic = get_models_by_tag('realistic')
        >>> for model in realistic:
        ...     print(model['name'])
    """
    return [
        model.copy()
        for model in AVAILABLE_MODELS
        if tag in model['tags']
    ]


def is_valid_model_id(model_id: str) -> bool:
    """
    Check if a model ID exists in the registry.
    
    Responsibility: ONLY validate model ID existence
    
    Args:
        model_id (str): Model identifier to check
    
    Returns:
        bool: True if model exists, False otherwise
    
    Example:
        >>> is_valid_model_id('black-forest-labs/FLUX.1-dev')
        True
        >>> is_valid_model_id('invalid-model')
        False
    """
    return any(model['id'] == model_id for model in AVAILABLE_MODELS)


def get_model_names_list() -> List[str]:
    """
    Get simple list of model names for display.
    
    Responsibility: ONLY extract and return model names
    
    Returns:
        List[str]: List of human-readable model names
    
    Example:
        >>> names = get_model_names_list()
        >>> print(names)
        ['FLUX.1 Dev', 'SDXL Lightning', ...]
    """
    return [model['name'] for model in AVAILABLE_MODELS]


def get_model_ids_list() -> List[str]:
    """
    Get simple list of model IDs.
    
    Responsibility: ONLY extract and return model IDs
    
    Returns:
        List[str]: List of model identifiers
    
    Example:
        >>> ids = get_model_ids_list()
        >>> print(ids[0])
        black-forest-labs/FLUX.1-dev
    """
    return [model['id'] for model in AVAILABLE_MODELS]


def get_default_parameters_for_model(model_id: str) -> Dict:
    """
    Get default generation parameters for a specific model.
    
    Responsibility: ONLY extract default parameters from model config
    
    Args:
        model_id (str): Model identifier
    
    Returns:
        Dict: Default parameters (width, height, steps, guidance)
    
    Raises:
        ValueError: If model_id is not found
    
    Example:
        >>> params = get_default_parameters_for_model('black-forest-labs/FLUX.1-dev')
        >>> print(params)
        {'width': 768, 'height': 768, 'steps': 30, 'guidance_scale': 7.5}
    """
    model = get_model_by_id(model_id)
    
    if not model:
        raise ValueError(f"Model '{model_id}' not found in registry")
    
    return {
        'width': model['default_width'],
        'height': model['default_height'],
        'num_inference_steps': model['default_steps'],
        'guidance_scale': model['default_guidance']
    }


def validate_parameters_for_model(model_id: str, parameters: Dict) -> Dict:
    """
    Validate and clamp parameters to model's supported ranges.
    
    Responsibility: ONLY validate params against model constraints
    
    Args:
        model_id (str): Model identifier
        parameters (Dict): Parameters to validate
    
    Returns:
        Dict: Validated parameters clamped to valid ranges
    
    Raises:
        ValueError: If model_id is not found
    
    Example:
        >>> params = {'width': 5000, 'steps': 5}
        >>> valid = validate_parameters_for_model('black-forest-labs/FLUX.1-dev', params)
        >>> print(valid['width'])  # Clamped to max
        2048
    """
    model = get_model_by_id(model_id)
    
    if not model:
        raise ValueError(f"Model '{model_id}' not found in registry")
    
    validated = {}
    
    # Validate and clamp width
    if 'width' in parameters:
        width = int(parameters['width'])
        validated['width'] = max(256, min(width, model['max_width']))
        # Ensure multiple of 8 (required by most diffusion models)
        validated['width'] = (validated['width'] // 8) * 8
    
    # Validate and clamp height
    if 'height' in parameters:
        height = int(parameters['height'])
        validated['height'] = max(256, min(height, model['max_height']))
        validated['height'] = (validated['height'] // 8) * 8
    
    # Validate and clamp steps
    if 'num_inference_steps' in parameters:
        steps = int(parameters['num_inference_steps'])
        validated['num_inference_steps'] = max(
            model['min_steps'],
            min(steps, model['max_steps'])
        )
    
    # Validate and clamp guidance scale
    if 'guidance_scale' in parameters:
        guidance = float(parameters['guidance_scale'])
        validated['guidance_scale'] = max(
            model['min_guidance'],
            min(guidance, model['max_guidance'])
        )
    
    # Pass through other supported parameters
    if 'seed' in parameters and model['supports_seed']:
        validated['seed'] = int(parameters['seed'])
    
    if 'negative_prompt' in parameters and model['supports_negative_prompt']:
        validated['negative_prompt'] = str(parameters['negative_prompt'])
    
    return validated
