/**
 * API Module
 * 
 * Handles all communication with the backend API.
 * Follows SRP - only responsible for API calls.
 * 
 * Each function has a single responsibility:
 * - Make HTTP request
 * - Handle response
 * - Return data or throw error
 */

const API = {
    /**
     * Fetch available models from the API.
     * 
     * Responsibility: ONLY fetch models list
     * 
     * @returns {Promise<Array>} Array of model objects
     * @throws {Error} If API request fails
     */
    async fetchModels() {
        try {
            const response = await fetch(
                `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.MODELS}?ui=true`
            );
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Failed to fetch models');
            }
            
            return data.models;
        } catch (error) {
            console.error('Error fetching models:', error);
            throw new Error(`Failed to load models: ${error.message}`);
        }
    },
    
    /**
     * Generate an image from parameters.
     * 
     * Responsibility: ONLY send generation request and return result
     * 
     * @param {Object} params - Generation parameters
     * @param {string} params.prompt - Text prompt
     * @param {string} params.model_id - Model identifier
     * @param {number} params.width - Image width
     * @param {number} params.height - Image height
     * @param {number} params.num_inference_steps - Number of steps
     * @param {number} params.guidance_scale - Guidance scale
     * @param {string} params.negative_prompt - Negative prompt (optional)
     * @param {number} params.seed - Random seed (optional)
     * 
     * @returns {Promise<Object>} Generation result with image and metadata
     * @throws {Error} If generation fails
     */
    async generateImage(params) {
        try {
            const response = await fetch(
                `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.GENERATE}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(params)
                }
            );
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Image generation failed');
            }
            
            return data;
        } catch (error) {
            console.error('Error generating image:', error);
            throw new Error(`Generation failed: ${error.message}`);
        }
    },
    
    /**
     * Check API health status.
     * 
     * Responsibility: ONLY check if API is responsive
     * 
     * @returns {Promise<Object>} Health status
     * @throws {Error} If health check fails
     */
    async checkHealth() {
        try {
            const response = await fetch(
                `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.HEALTH}`
            );
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Health check failed:', error);
            throw new Error(`API unavailable: ${error.message}`);
        }
    }
};

// Make API available globally
window.API = API;
