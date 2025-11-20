"""
Main Flask Application

This is the entry point for the image generation API server.
It sets up routes, handles requests, and coordinates between services.

Follows SOLID principles:
- Routes are clean and delegate to services
- Each route has a single responsibility
- Services are injected as dependencies

Usage:
    python app.py
"""

import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from config import config
from services.image_service import ImageGenerationService
from services.model_service import ModelService


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize Flask application
app = Flask(__name__, static_folder='../frontend')

# Enable CORS to allow frontend to communicate with backend
# In production, you should restrict this to your frontend domain
CORS(app)


# Initialize services with dependency injection
# These are created once when the app starts
try:
    image_service = ImageGenerationService(api_key=config.HF_TOKEN)
    model_service = ModelService()
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {str(e)}")
    raise


# ============================================================================
# ROUTE: Serve Frontend
# ============================================================================

@app.route('/')
def serve_frontend():
    """
    Serve the main HTML page.
    
    Responsibility: ONLY serve the frontend index file
    
    Returns:
        HTML file
    """
    return send_from_directory('../frontend', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """
    Serve static files (CSS, JS, images).
    
    Responsibility: ONLY serve static assets
    
    Args:
        path (str): File path relative to frontend directory
    
    Returns:
        Static file
    """
    return send_from_directory('../frontend', path)


# ============================================================================
# ROUTE: Health Check
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Check if the API is running and healthy.
    
    Responsibility: ONLY verify system health
    
    Returns:
        JSON: Health status information
    
    Example response:
        {
            "status": "healthy",
            "services": {
                "api": "running",
                "huggingface": "connected"
            }
        }
    """
    try:
        # Test HuggingFace connection
        hf_status = "connected" if image_service.test_connection() else "disconnected"
        
        return jsonify({
            'status': 'healthy',
            'services': {
                'api': 'running',
                'huggingface': hf_status
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


# ============================================================================
# ROUTE: Get Available Models
# ============================================================================

@app.route('/api/models', methods=['GET'])
def get_models():
    """
    Get list of available image generation models.
    
    Responsibility: ONLY retrieve and return model list
    
    Query Parameters:
        category (optional): Filter by category
        tag (optional): Filter by tag
        ui (optional): If 'true', returns simplified UI-optimized list
    
    Returns:
        JSON: List of models with their details
    
    Example:
        GET /api/models
        GET /api/models?category=fast
        GET /api/models?ui=true
    """
    try:
        # Check for query parameters
        category = request.args.get('category')
        tag = request.args.get('tag')
        ui_mode = request.args.get('ui', '').lower() == 'true'
        
        # Get models based on filters
        if category:
            models = model_service.get_models_by_category(category)
        elif tag:
            models = model_service.get_models_by_tag(tag)
        elif ui_mode:
            models = model_service.get_models_for_ui()
        else:
            models = model_service.get_available_models()
        
        return jsonify({
            'success': True,
            'models': models,
            'count': len(models)
        }), 200
    
    except Exception as e:
        logger.error(f"Failed to get models: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ROUTE: Get Model Details
# ============================================================================

@app.route('/api/models/<path:model_id>', methods=['GET'])
def get_model_details(model_id):
    """
    Get detailed information about a specific model.
    
    Responsibility: ONLY retrieve single model details
    
    Args:
        model_id (str): Model identifier (URL-encoded)
    
    Returns:
        JSON: Model details
    
    Example:
        GET /api/models/black-forest-labs/FLUX.1-dev
    """
    try:
        model = model_service.get_model_details(model_id)
        
        if model:
            return jsonify({
                'success': True,
                'model': model
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f"Model '{model_id}' not found"
            }), 404
    
    except Exception as e:
        logger.error(f"Failed to get model details: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ROUTE: Generate Image
# ============================================================================

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """
    Generate an image from a text prompt.
    
    Responsibility: ONLY coordinate image generation request
    
    Request Body (JSON):
        {
            "prompt": "A beautiful sunset",
            "model_id": "black-forest-labs/FLUX.1-dev",
            "width": 768,
            "height": 768,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "negative_prompt": "blurry, low quality",
            "seed": 42
        }
    
    Returns:
        JSON: Generated image (base64) and metadata
    
    Example response:
        {
            "success": true,
            "image": "base64_encoded_image...",
            "metadata": {
                "model_id": "...",
                "prompt": "...",
                "width": 768,
                "height": 768,
                "timestamp": "..."
            }
        }
    """
    try:
        # Parse request body
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Extract required parameters
        prompt = data.get('prompt')
        model_id = data.get('model_id')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            }), 400
        
        if not model_id:
            return jsonify({
                'success': False,
                'error': 'Model ID is required'
            }), 400
        
        # Validate model exists
        if not model_service.validate_model_id(model_id):
            return jsonify({
                'success': False,
                'error': f"Invalid model ID: '{model_id}'"
            }), 400
        
        # Extract optional parameters
        width = data.get('width', 768)
        height = data.get('height', 768)
        num_inference_steps = data.get('num_inference_steps')
        guidance_scale = data.get('guidance_scale')
        negative_prompt = data.get('negative_prompt')
        seed = data.get('seed')
        
        # Validate and prepare parameters for the model
        params = {
            'width': width,
            'height': height
        }
        
        if num_inference_steps is not None:
            params['num_inference_steps'] = num_inference_steps
        
        if guidance_scale is not None:
            params['guidance_scale'] = guidance_scale
        
        if negative_prompt:
            params['negative_prompt'] = negative_prompt
        
        if seed is not None:
            params['seed'] = seed
        
        # Validate parameters against model constraints
        validated_params = model_service.validate_and_prepare_parameters(
            model_id,
            params
        )
        
        logger.info(f"Generating image with model: {model_id}")
        
        # Generate image
        result = image_service.generate_image(
            prompt=prompt,
            model_id=model_id,
            **validated_params
        )
        
        # Return result
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except ValueError as e:
        # Validation errors
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        # Unexpected errors
        logger.error(f"Image generation failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ROUTE: Get Model Summary
# ============================================================================

@app.route('/api/models/summary', methods=['GET'])
def get_model_summary():
    """
    Get summary statistics about available models.
    
    Responsibility: ONLY return model statistics
    
    Returns:
        JSON: Model summary with counts and categories
    """
    try:
        summary = model_service.get_model_summary()
        
        return jsonify({
            'success': True,
            'summary': summary
        }), 200
    
    except Exception as e:
        logger.error(f"Failed to get model summary: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.
    
    Responsibility: ONLY format 404 response
    """
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors.
    
    Responsibility: ONLY format 500 response
    """
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == '__main__':
    """
    Start the Flask development server.
    
    This runs when you execute: python app.py
    """
    try:
        # Validate configuration before starting
        config.validate()
        
        logger.info(f"Starting server on {config.HOST}:{config.PORT}")
        logger.info(f"Debug mode: {config.DEBUG}")
        
        # Start Flask development server
        # WARNING: This is for development only!
        # In production, use a proper WSGI server like Gunicorn
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )
    
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
