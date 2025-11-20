"""
Model Management Service Module

This module provides a service layer for model-related operations.
It acts as a bridge between the API routes and the model configuration.

Follows Single Responsibility Principle - only handles model information
and management, not image generation.

Usage:
    from services.model_service import ModelService
    
    service = ModelService()
    models = service.get_available_models()
"""

import logging
from typing import Dict, List, Optional

from models.models_config import (
    get_all_models,
    get_model_by_id,
    get_models_by_category,
    get_models_by_tag,
    is_valid_model_id,
    get_default_parameters_for_model,
    validate_parameters_for_model
)


# Configure logging for this module
logger = logging.getLogger(__name__)


class ModelService:
    """
    Service for managing model information and operations.
    
    This class provides a clean interface for model-related queries
    and operations, abstracting the underlying model configuration.
    
    Example:
        service = ModelService()
        models = service.get_available_models()
        model_info = service.get_model_details('black-forest-labs/FLUX.1-dev')
    """
    
    def __init__(self):
        """
        Initialize the model service.
        
        Responsibility: ONLY set up the service (currently no setup needed)
        """
        logger.info("ModelService initialized successfully")
    
    def get_available_models(self) -> List[Dict]:
        """
        Get list of all available models.
        
        Responsibility: ONLY retrieve and return available models
        
        Returns:
            List[Dict]: List of all model configurations
        
        Example:
            >>> service = ModelService()
            >>> models = service.get_available_models()
            >>> print(f"Found {len(models)} models")
        """
        logger.debug("Retrieving all available models")
        models = get_all_models()
        logger.info(f"Retrieved {len(models)} available models")
        return models
    
    def get_model_details(self, model_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific model.
        
        Responsibility: ONLY retrieve model details by ID
        
        Args:
            model_id (str): Model identifier
        
        Returns:
            Optional[Dict]: Model details if found, None otherwise
        
        Example:
            >>> service = ModelService()
            >>> model = service.get_model_details('black-forest-labs/FLUX.1-dev')
            >>> print(model['name'])
            FLUX.1 Dev
        """
        logger.debug(f"Retrieving details for model: {model_id}")
        model = get_model_by_id(model_id)
        
        if model:
            logger.info(f"Found model: {model['name']}")
        else:
            logger.warning(f"Model not found: {model_id}")
        
        return model
    
    def get_models_by_category(self, category: str) -> List[Dict]:
        """
        Get models filtered by category.
        
        Responsibility: ONLY retrieve models in specific category
        
        Args:
            category (str): Category name ('general', 'fast', 'artistic', etc.)
        
        Returns:
            List[Dict]: Models in the specified category
        
        Example:
            >>> service = ModelService()
            >>> fast_models = service.get_models_by_category('fast')
        """
        logger.debug(f"Retrieving models in category: {category}")
        models = get_models_by_category(category)
        logger.info(f"Found {len(models)} models in category '{category}'")
        return models
    
    def get_models_by_tag(self, tag: str) -> List[Dict]:
        """
        Get models filtered by tag.
        
        Responsibility: ONLY retrieve models with specific tag
        
        Args:
            tag (str): Tag name ('realistic', 'fast', 'artistic', etc.)
        
        Returns:
            List[Dict]: Models with the specified tag
        
        Example:
            >>> service = ModelService()
            >>> realistic = service.get_models_by_tag('realistic')
        """
        logger.debug(f"Retrieving models with tag: {tag}")
        models = get_models_by_tag(tag)
        logger.info(f"Found {len(models)} models with tag '{tag}'")
        return models
    
    def validate_model_id(self, model_id: str) -> bool:
        """
        Check if a model ID is valid.
        
        Responsibility: ONLY validate model ID existence
        
        Args:
            model_id (str): Model identifier to validate
        
        Returns:
            bool: True if model exists, False otherwise
        
        Example:
            >>> service = ModelService()
            >>> is_valid = service.validate_model_id('black-forest-labs/FLUX.1-dev')
            >>> print(is_valid)
            True
        """
        is_valid = is_valid_model_id(model_id)
        
        if is_valid:
            logger.debug(f"Model ID validated: {model_id}")
        else:
            logger.warning(f"Invalid model ID: {model_id}")
        
        return is_valid
    
    def get_default_parameters(self, model_id: str) -> Dict:
        """
        Get default generation parameters for a model.
        
        Responsibility: ONLY retrieve default parameters
        
        Args:
            model_id (str): Model identifier
        
        Returns:
            Dict: Default parameters for the model
        
        Raises:
            ValueError: If model_id is not found
        
        Example:
            >>> service = ModelService()
            >>> params = service.get_default_parameters('black-forest-labs/FLUX.1-dev')
            >>> print(params['width'])
            768
        """
        logger.debug(f"Getting default parameters for: {model_id}")
        
        try:
            params = get_default_parameters_for_model(model_id)
            logger.info(f"Retrieved default parameters for {model_id}")
            return params
        
        except ValueError as e:
            logger.error(f"Failed to get default parameters: {str(e)}")
            raise
    
    def validate_and_prepare_parameters(
        self,
        model_id: str,
        parameters: Dict
    ) -> Dict:
        """
        Validate parameters against model constraints.
        
        Responsibility: ONLY validate and clamp parameters
        
        Args:
            model_id (str): Model identifier
            parameters (Dict): Parameters to validate
        
        Returns:
            Dict: Validated parameters clamped to valid ranges
        
        Raises:
            ValueError: If model_id is not found
        
        Example:
            >>> service = ModelService()
            >>> params = {'width': 5000, 'steps': 5}
            >>> valid = service.validate_and_prepare_parameters(
            ...     'black-forest-labs/FLUX.1-dev',
            ...     params
            ... )
        """
        logger.debug(f"Validating parameters for model: {model_id}")
        
        try:
            validated = validate_parameters_for_model(model_id, parameters)
            logger.info(f"Parameters validated for {model_id}")
            return validated
        
        except ValueError as e:
            logger.error(f"Parameter validation failed: {str(e)}")
            raise
    
    def get_model_summary(self) -> Dict:
        """
        Get summary statistics about available models.
        
        Responsibility: ONLY calculate and return model statistics
        
        Returns:
            Dict: Summary with counts by category, tags, etc.
        
        Example:
            >>> service = ModelService()
            >>> summary = service.get_model_summary()
            >>> print(summary['total_models'])
            5
        """
        logger.debug("Generating model summary")
        
        models = get_all_models()
        
        # Count models by category
        categories = {}
        for model in models:
            cat = model['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        # Count models by provider
        providers = {}
        for model in models:
            prov = model['provider']
            providers[prov] = providers.get(prov, 0) + 1
        
        # Collect all unique tags
        all_tags = set()
        for model in models:
            all_tags.update(model['tags'])
        
        summary = {
            'total_models': len(models),
            'categories': categories,
            'providers': providers,
            'unique_tags': sorted(list(all_tags))
        }
        
        logger.info(f"Generated summary for {summary['total_models']} models")
        return summary
    
    def get_models_for_ui(self) -> List[Dict]:
        """
        Get simplified model list optimized for UI display.
        
        Responsibility: ONLY format models for frontend consumption
        
        Returns:
            List[Dict]: Simplified model list with essential info
        
        Note:
            This returns only the fields needed by the UI,
            reducing payload size and complexity.
        
        Example:
            >>> service = ModelService()
            >>> ui_models = service.get_models_for_ui()
        """
        logger.debug("Preparing models for UI")
        
        models = get_all_models()
        
        # Extract only fields needed by UI
        ui_models = []
        for model in models:
            ui_models.append({
                'id': model['id'],
                'name': model['name'],
                'description': model['description'],
                'category': model['category'],
                'estimated_time': model['estimated_time'],
                'tags': model['tags'],
                'default_params': {
                    'width': model['default_width'],
                    'height': model['default_height'],
                    'steps': model['default_steps'],
                    'guidance': model['default_guidance']
                }
            })
        
        logger.info(f"Prepared {len(ui_models)} models for UI")
        return ui_models
    
    def search_models(self, query: str) -> List[Dict]:
        """
        Search models by name, description, or tags.
        
        Responsibility: ONLY search and filter models
        
        Args:
            query (str): Search query
        
        Returns:
            List[Dict]: Models matching the search query
        
        Example:
            >>> service = ModelService()
            >>> results = service.search_models('fast')
        """
        logger.debug(f"Searching models with query: {query}")
        
        if not query:
            return get_all_models()
        
        query_lower = query.lower()
        models = get_all_models()
        results = []
        
        for model in models:
            # Search in name
            if query_lower in model['name'].lower():
                results.append(model)
                continue
            
            # Search in description
            if query_lower in model['description'].lower():
                results.append(model)
                continue
            
            # Search in tags
            if any(query_lower in tag.lower() for tag in model['tags']):
                results.append(model)
                continue
        
        logger.info(f"Found {len(results)} models matching '{query}'")
        return results
