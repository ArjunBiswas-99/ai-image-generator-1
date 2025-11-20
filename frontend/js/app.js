/**
 * Main Application Module
 * 
 * Orchestrates the application by connecting UI, API, and user interactions.
 * Follows SRP - each function handles a specific application concern.
 * 
 * Application flow:
 * 1. Initialize on page load
 * 2. Load models and setup event listeners
 * 3. Handle user interactions
 * 4. Coordinate between UI and API modules
 */

const App = {
    // Store loaded models for reference
    models: [],
    
    // Store current generation result
    currentImage: null,
    currentMetadata: null,
    
    /**
     * Initialize the application.
     * 
     * Responsibility: ONLY coordinate initialization tasks
     */
    async init() {
        console.log('Initializing HuggingFace Image Generator...');
        
        try {
            // Load saved theme
            UI.loadTheme();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Load models from API
            await this.loadModels();
            
            // Update status
            UI.updateStatus('Ready');
            
            console.log('Application initialized successfully');
        } catch (error) {
            console.error('Initialization error:', error);
            UI.showError(`Failed to initialize: ${error.message}`);
            UI.updateStatus('Error');
        }
    },
    
    /**
     * Load available models from API.
     * 
     * Responsibility: ONLY fetch and populate models
     */
    async loadModels() {
        try {
            UI.updateStatus('Loading models...');
            
            // Fetch models from API
            this.models = await API.fetchModels();
            
            // Populate UI dropdown
            UI.populateModels(this.models);
            
            console.log(`Loaded ${this.models.length} models`);
        } catch (error) {
            throw new Error(`Failed to load models: ${error.message}`);
        }
    },
    
    /**
     * Setup all event listeners.
     * 
     * Responsibility: ONLY attach event handlers
     */
    setupEventListeners() {
        // Generate button
        document.getElementById('generate-btn').addEventListener('click', () => {
            this.handleGenerate();
        });
        
        // Model selection change
        document.getElementById('model-select').addEventListener('change', (e) => {
            this.handleModelChange(e.target.value);
        });
        
        // Prompt character count
        document.getElementById('prompt').addEventListener('input', (e) => {
            UI.updateCharCount('prompt-length', e.target.value.length);
        });
        
        // Negative prompt character count
        document.getElementById('negative-prompt').addEventListener('input', (e) => {
            UI.updateCharCount('negative-prompt-length', e.target.value.length);
        });
        
        // Steps slider
        document.getElementById('steps').addEventListener('input', (e) => {
            UI.updateSliderValue('steps-value', e.target.value);
        });
        
        // Guidance slider
        document.getElementById('guidance').addEventListener('input', (e) => {
            UI.updateSliderValue('guidance-value', e.target.value);
        });
        
        // Random seed button
        document.getElementById('random-seed').addEventListener('click', () => {
            UI.generateRandomSeed();
        });
        
        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => {
            UI.toggleTheme();
        });
        
        // Download button
        document.getElementById('download-btn').addEventListener('click', () => {
            this.handleDownload();
        });
        
        // Copy prompt button
        document.getElementById('copy-prompt-btn').addEventListener('click', () => {
            this.handleCopyPrompt();
        });
        
        // Regenerate button
        document.getElementById('regenerate-btn').addEventListener('click', () => {
            this.handleGenerate();
        });
    },
    
    /**
     * Handle model selection change.
     * 
     * Responsibility: ONLY update UI for selected model
     * 
     * @param {string} modelId - Selected model ID
     */
    handleModelChange(modelId) {
        const model = this.models.find(m => m.id === modelId);
        if (model) {
            UI.updateModelDescription(model);
            
            // Update default parameters
            document.getElementById('steps').value = model.default_params.steps;
            UI.updateSliderValue('steps-value', model.default_params.steps);
            
            document.getElementById('guidance').value = model.default_params.guidance;
            UI.updateSliderValue('guidance-value', model.default_params.guidance);
        }
    },
    
    /**
     * Handle image generation request.
     * 
     * Responsibility: ONLY coordinate generation process
     */
    async handleGenerate() {
        try {
            // Get form values
            const params = this.getGenerationParameters();
            
            // Validate prompt
            if (!params.prompt || params.prompt.trim().length === 0) {
                UI.showError('Please enter a prompt');
                return;
            }
            
            // Update UI state
            UI.updateStatus('Generating', true);
            UI.setGenerateButtonEnabled(false);
            UI.showLoading();
            
            console.log('Generating image with params:', params);
            
            // Call API
            const result = await API.generateImage(params);
            
            // Store result
            this.currentImage = result.image;
            this.currentMetadata = result.metadata;
            
            // Update UI with result
            UI.hideLoading();
            UI.displayImage(result.image);
            UI.updateMetadata(result.metadata);
            UI.addToGallery(result.image, result.metadata);
            
            // Save to gallery storage
            this.saveToGalleryStorage(result.image, result.metadata);
            
            // Update status
            UI.updateStatus('Ready', false);
            UI.showSuccess('Image generated successfully!');
            
        } catch (error) {
            console.error('Generation error:', error);
            UI.hideLoading();
            UI.updateStatus('Error', false);
            UI.showError(error.message);
        } finally {
            UI.setGenerateButtonEnabled(true);
        }
    },
    
    /**
     * Get generation parameters from form.
     * 
     * Responsibility: ONLY read and format form values
     * 
     * @returns {Object} Generation parameters
     */
    getGenerationParameters() {
        const prompt = document.getElementById('prompt').value;
        const modelId = document.getElementById('model-select').value;
        const size = UI.getSelectedSize();
        const steps = parseInt(document.getElementById('steps').value);
        const guidance = parseFloat(document.getElementById('guidance').value);
        const negativePrompt = document.getElementById('negative-prompt').value;
        const seedInput = document.getElementById('seed').value;
        
        const params = {
            prompt: prompt,
            model_id: modelId,
            width: size,
            height: size,
            num_inference_steps: steps,
            guidance_scale: guidance
        };
        
        // Add optional parameters
        if (negativePrompt && negativePrompt.trim().length > 0) {
            params.negative_prompt = negativePrompt;
        }
        
        if (seedInput && seedInput.trim().length > 0) {
            params.seed = parseInt(seedInput);
        }
        
        return params;
    },
    
    /**
     * Handle image download.
     * 
     * Responsibility: ONLY trigger download of current image
     */
    handleDownload() {
        if (!this.currentImage) {
            UI.showError('No image to download');
            return;
        }
        
        // Generate filename with timestamp
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `hf-generated-${timestamp}.png`;
        
        UI.downloadImage(this.currentImage, filename);
        UI.showSuccess('Image downloaded!');
    },
    
    /**
     * Handle copy prompt to clipboard.
     * 
     * Responsibility: ONLY copy current prompt
     */
    handleCopyPrompt() {
        const prompt = document.getElementById('prompt').value;
        
        if (!prompt || prompt.trim().length === 0) {
            UI.showError('No prompt to copy');
            return;
        }
        
        UI.copyToClipboard(prompt);
    },
    
    /**
     * Save generated image to local storage gallery.
     * 
     * Responsibility: ONLY persist image to storage
     * 
     * @param {string} image - Base64 image
     * @param {Object} metadata - Image metadata
     */
    saveToGalleryStorage(image, metadata) {
        try {
            // Get existing gallery
            const galleryJson = localStorage.getItem(CONFIG.STORAGE.GALLERY);
            let gallery = galleryJson ? JSON.parse(galleryJson) : [];
            
            // Add new item at beginning
            gallery.unshift({
                image: image,
                metadata: metadata,
                timestamp: new Date().toISOString()
            });
            
            // Limit gallery size
            if (gallery.length > CONFIG.UI.MAX_GALLERY_ITEMS) {
                gallery = gallery.slice(0, CONFIG.UI.MAX_GALLERY_ITEMS);
            }
            
            // Save back to storage
            localStorage.setItem(CONFIG.STORAGE.GALLERY, JSON.stringify(gallery));
        } catch (error) {
            console.error('Failed to save to gallery storage:', error);
            // Don't show error to user, this is non-critical
        }
    },
    
    /**
     * Load gallery from local storage.
     * 
     * Responsibility: ONLY load persisted gallery
     */
    loadGalleryFromStorage() {
        try {
            const galleryJson = localStorage.getItem(CONFIG.STORAGE.GALLERY);
            if (!galleryJson) return;
            
            const gallery = JSON.parse(galleryJson);
            
            // Add each item to gallery UI
            gallery.forEach(item => {
                UI.addToGallery(item.image, item.metadata);
            });
        } catch (error) {
            console.error('Failed to load gallery from storage:', error);
            // Don't show error to user, this is non-critical
        }
    }
};

// Initialize application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        App.init();
    });
} else {
    // DOM already loaded
    App.init();
}

// Make App available globally for debugging
window.App = App;
