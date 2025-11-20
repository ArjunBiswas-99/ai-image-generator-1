/**
 * Configuration Module
 * 
 * Contains application configuration and constants.
 * Follows SRP - only manages configuration values.
 */

const CONFIG = {
    // API Configuration
    API_BASE_URL: 'http://localhost:5000',
    
    // API Endpoints
    ENDPOINTS: {
        MODELS: '/api/models',
        GENERATE: '/api/generate',
        HEALTH: '/api/health'
    },
    
    // Default Generation Parameters
    DEFAULTS: {
        MODEL: 'black-forest-labs/FLUX.1-dev',
        WIDTH: 768,
        HEIGHT: 768,
        STEPS: 30,
        GUIDANCE: 7.5
    },
    
    // UI Configuration
    UI: {
        TOAST_DURATION: 5000, // milliseconds
        MAX_GALLERY_ITEMS: 10,
        THEME_STORAGE_KEY: 'hf-generator-theme'
    },
    
    // Local Storage Keys
    STORAGE: {
        GALLERY: 'hf-generator-gallery',
        LAST_PARAMS: 'hf-generator-last-params'
    }
};

// Make config available globally
window.CONFIG = CONFIG;
