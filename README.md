# ai-image-generator-1
## 📁 Project Structure

```javascript
ai-image-generator-1/
├── backend/               # Python Flask backend
│   ├── app.py            # Main application with routes
│   ├── config.py         # Environment configuration
│   ├── requirements.txt  # Python dependencies
│   ├── .env.example      # Environment template
│   ├── services/         # Business logic
│   ├── models/           # Model definitions
│   └── utils/            # Validators & helpers
└── frontend/             # HTML/CSS/JavaScript frontend
    ├── index.html        # Main page
    ├── css/style.css     # Modern dark theme styling
    └── js/               # Modular JavaScript
        ├── config.js     # Configuration
        ├── api.js        # API calls
        ├── ui.js         # UI updates
        └── app.js        # Main logic
```

## 🚀 How to Test Locally

### Step 1: Get HuggingFace Token

1. Visit: [](https://huggingface.co/settings/tokens/new)<https://huggingface.co/settings/tokens/new>
2. Create __Fine-grained__ token with __"Make calls to Inference Providers"__ permission
3. Copy your token (starts with `hf_`)

### Step 2: Setup Backend

```bash
cd ai-image-generator-1/backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your HF_TOKEN
```

### Step 3: Start Server

```bash
python app.py
```

Server runs on: [](http://localhost:5000)<http://localhost:5000>

### Step 4: Test the Application

Open browser to: [](http://localhost:5000)<http://localhost:5000>

__Test Flow:__

1. Enter prompt: "A serene lake surrounded by mountains at sunset"
2. Select model (FLUX.1 Dev is default)
3. Adjust parameters if desired
4. Click "Generate Image"
5. Wait 15-30 seconds
6. Image appears with download/copy options

## ✨ Features Implemented

- ✅ 5 free HuggingFace models (FLUX.1, SDXL, Hyper-SD, etc.)
- ✅ Advanced parameters (steps, guidance, seed, negative prompt)
- ✅ Dark/light theme toggle
- ✅ Local image gallery with localStorage
- ✅ Download images
- ✅ Copy prompts to clipboard
- ✅ Responsive design
- ✅ Error handling & validation
- ✅ Loading states & animations

## 📦 Dependencies

__Backend:__

- Flask 3.0.0
- flask-cors 4.0.0
- huggingface-hub 0.20.0
- Pillow 10.1.0
- python-dotenv 1.0.0

__Frontend:__

- Vanilla JavaScript (no frameworks needed)
- Modern CSS with CSS variables
- HTML5

## 🎓 Learning Python

The code is designed to be educational:

- Extensive comments explaining every function
- Clear function names describing purpose
- Type hints for better understanding
- Single responsibility principle throughout
- Easy-to-follow structure

Perfect for learning Python web development!

## 🔧 Troubleshooting

__Port 5000 in use:__

- Change PORT in .env file

__API errors:__

- Verify HF_TOKEN in .env
- Check token has correct permissions
- Ensure you have free tier credits

__Frontend not loading:__

- Verify backend is running
- Check browser console for errors
- Try [](http://127.0.0.1:5000)<http://127.0.0.1:5000>

The application is production-ready and follows best practices throughout!
