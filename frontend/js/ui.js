/**
 * UI Module
 * 
 * Handles all user interface updates and DOM manipulations.
 * Follows SRP - only responsible for UI updates, not business logic.
 * 
 * Each function has a single responsibility:
 * - Update specific UI element
 * - Show/hide specific component
 * - Handle specific visual state
 */

const UI = {
    /**
     * Show error toast notification.
     * 
     * Responsibility: ONLY display error message
     * 
     * @param {string} message - Error message to display
     */
    showError(message) {
        const toast = document.getElementById('error-toast');
        const messageEl = document.getElementById('error-message');
        
        messageEl.textContent = message;
        toast.style.display = 'flex';
        
        // Auto-hide after duration
        setTimeout(() => {
            this.hideError();
        }, CONFIG.UI.TOAST_DURATION);
    },
    
    /**
     * Hide error toast.
     * 
     * Responsibility: ONLY hide error toast
     */
    hideError() {
        const toast = document.getElementById('error-toast');
        toast.style.display = 'none';
    },
    
    /**
     * Show success toast notification.
     * 
     * Responsibility: ONLY display success message
     * 
     * @param {string} message - Success message to display
     */
    showSuccess(message) {
        const toast = document.getElementById('success-toast');
        const messageEl = document.getElementById('success-message');
        
        messageEl.textContent = message;
        toast.style.display = 'flex';
        
        // Auto-hide after duration
        setTimeout(() => {
            this.hideSuccess();
        }, CONFIG.UI.TOAST_DURATION);
    },
    
    /**
     * Hide success toast.
     * 
     * Responsibility: ONLY hide success toast
     */
    hideSuccess() {
        const toast = document.getElementById('success-toast');
        toast.style.display = 'none';
    },
    
    /**
     * Update status indicator.
     * 
     * Responsibility: ONLY update status text and style
     * 
     * @param {string} status - Status text
     * @param {boolean} isGenerating - Whether currently generating
     */
    updateStatus(status, isGenerating = false) {
        const statusEl = document.getElementById('status-indicator');
        statusEl.textContent = status;
        
        if (isGenerating) {
            statusEl.classList.add('generating');
        } else {
            statusEl.classList.remove('generating');
        }
    },
    
    /**
     * Populate model dropdown with options.
     * 
     * Responsibility: ONLY populate select element
     * 
     * @param {Array} models - Array of model objects
     */
    populateModels(models) {
        const select = document.getElementById('model-select');
        select.innerHTML = '';
        
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.id;
            option.textContent = model.name;
            select.appendChild(option);
        });
        
        // Update description for first model
        if (models.length > 0) {
            this.updateModelDescription(models[0]);
        }
    },
    
    /**
     * Update model description text.
     * 
     * Responsibility: ONLY update description display
     * 
     * @param {Object} model - Model object
     */
    updateModelDescription(model) {
        const descEl = document.getElementById('model-description');
        descEl.textContent = `${model.description} • Est. time: ${model.estimated_time}`;
        
        const currentModelEl = document.getElementById('current-model');
        currentModelEl.textContent = model.name;
    },
    
    /**
     * Show loading overlay on image container.
     * 
     * Responsibility: ONLY show loading state
     */
    showLoading() {
        const loading = document.getElementById('loading-overlay');
        const placeholder = document.querySelector('.placeholder');
        
        if (placeholder) {
            placeholder.style.display = 'none';
        }
        
        loading.style.display = 'flex';
    },
    
    /**
     * Hide loading overlay.
     * 
     * Responsibility: ONLY hide loading state
     */
    hideLoading() {
        const loading = document.getElementById('loading-overlay');
        loading.style.display = 'none';
    },
    
    /**
     * Display generated image.
     * 
     * Responsibility: ONLY update image display
     * 
     * @param {string} base64Image - Base64 encoded image
     */
    displayImage(base64Image) {
        const img = document.getElementById('generated-image');
        const placeholder = document.querySelector('.placeholder');
        
        // Hide placeholder
        if (placeholder) {
            placeholder.style.display = 'none';
        }
        
        // Set image source and show
        img.src = `data:image/png;base64,${base64Image}`;
        img.style.display = 'block';
        
        // Show action buttons
        document.getElementById('image-actions').style.display = 'flex';
    },
    
    /**
     * Update image metadata display.
     * 
     * Responsibility: ONLY update metadata text
     * 
     * @param {Object} metadata - Image metadata
     */
    updateMetadata(metadata) {
        const metadataEl = document.getElementById('image-metadata');
        const modelEl = document.getElementById('meta-model');
        const sizeEl = document.getElementById('meta-size');
        const stepsEl = document.getElementById('meta-steps');
        const timeEl = document.getElementById('meta-time');
        
        modelEl.textContent = metadata.model_id.split('/').pop();
        sizeEl.textContent = `${metadata.width}x${metadata.height}`;
        stepsEl.textContent = metadata.parameters.num_inference_steps || 'N/A';
        timeEl.textContent = new Date(metadata.timestamp).toLocaleTimeString();
        
        metadataEl.style.display = 'block';
    },
    
    /**
     * Add image to gallery.
     * 
     * Responsibility: ONLY add gallery item
     * 
     * @param {string} base64Image - Base64 encoded image
     * @param {Object} metadata - Image metadata
     */
    addToGallery(base64Image, metadata) {
        const gallery = document.getElementById('gallery');
        const emptyMsg = gallery.querySelector('.gallery-empty');
        
        // Remove empty message if present
        if (emptyMsg) {
            emptyMsg.remove();
        }
        
        // Create gallery item
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.title = metadata.prompt;
        
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${base64Image}`;
        img.alt = metadata.prompt;
        
        // Click to load in main view
        item.addEventListener('click', () => {
            this.displayImage(base64Image);
            this.updateMetadata(metadata);
        });
        
        item.appendChild(img);
        gallery.insertBefore(item, gallery.firstChild);
        
        // Limit gallery size
        const items = gallery.querySelectorAll('.gallery-item');
        if (items.length > CONFIG.UI.MAX_GALLERY_ITEMS) {
            items[items.length - 1].remove();
        }
    },
    
    /**
     * Enable/disable generate button.
     * 
     * Responsibility: ONLY update button state
     * 
     * @param {boolean} enabled - Whether button should be enabled
     */
    setGenerateButtonEnabled(enabled) {
        const btn = document.getElementById('generate-btn');
        btn.disabled = !enabled;
        
        if (enabled) {
            btn.textContent = '🎨 Generate Image';
        } else {
            btn.textContent = '⏳ Generating...';
        }
    },
    
    /**
     * Update character count display.
     * 
     * Responsibility: ONLY update counter text
     * 
     * @param {string} elementId - ID of counter element
     * @param {number} count - Current character count
     */
    updateCharCount(elementId, count) {
        const el = document.getElementById(elementId);
        el.textContent = count;
    },
    
    /**
     * Update slider value display.
     * 
     * Responsibility: ONLY update slider value text
     * 
     * @param {string} elementId - ID of value display element
     * @param {number} value - Current slider value
     */
    updateSliderValue(elementId, value) {
        const el = document.getElementById(elementId);
        el.textContent = value;
    },
    
    /**
     * Get selected image size.
     * 
     * Responsibility: ONLY read size from radio buttons
     * 
     * @returns {number} Selected size value
     */
    getSelectedSize() {
        const radio = document.querySelector('input[name="size"]:checked');
        return parseInt(radio.value);
    },
    
    /**
     * Toggle theme between dark and light.
     * 
     * Responsibility: ONLY toggle theme class
     */
    toggleTheme() {
        document.body.classList.toggle('light-theme');
        
        // Save preference
        const isLight = document.body.classList.contains('light-theme');
        localStorage.setItem(CONFIG.UI.THEME_STORAGE_KEY, isLight ? 'light' : 'dark');
        
        // Update icon
        const icon = document.querySelector('.theme-icon');
        icon.textContent = isLight ? '☀️' : '🌙';
    },
    
    /**
     * Load saved theme preference.
     * 
     * Responsibility: ONLY apply saved theme
     */
    loadTheme() {
        const savedTheme = localStorage.getItem(CONFIG.UI.THEME_STORAGE_KEY);
        
        if (savedTheme === 'light') {
            document.body.classList.add('light-theme');
            const icon = document.querySelector('.theme-icon');
            icon.textContent = '☀️';
        }
    },
    
    /**
     * Generate random seed and update input.
     * 
     * Responsibility: ONLY generate and display random number
     */
    generateRandomSeed() {
        const seedInput = document.getElementById('seed');
        const randomSeed = Math.floor(Math.random() * (2**32));
        seedInput.value = randomSeed;
    },
    
    /**
     * Download image to user's computer.
     * 
     * Responsibility: ONLY trigger download
     * 
     * @param {string} base64Image - Base64 encoded image
     * @param {string} filename - Desired filename
     */
    downloadImage(base64Image, filename = 'generated-image.png') {
        const link = document.createElement('a');
        link.href = `data:image/png;base64,${base64Image}`;
        link.download = filename;
        link.click();
    },
    
    /**
     * Copy text to clipboard.
     * 
     * Responsibility: ONLY copy text to clipboard
     * 
     * @param {string} text - Text to copy
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showSuccess('Copied to clipboard!');
        } catch (error) {
            this.showError('Failed to copy to clipboard');
        }
    }
};

// Make UI available globally
window.UI = UI;

// Make hideError and hideSuccess available globally for inline onclick
window.hideError = () => UI.hideError();
window.hideSuccess = () => UI.hideSuccess();
