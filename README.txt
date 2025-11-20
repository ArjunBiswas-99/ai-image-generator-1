===============================================================================
                      BASIC AI IMAGE GENERATOR
              Free AI Image Generation with Multiple Models
===============================================================================

WHAT IS THIS?
=============
A web-based image generator that uses HuggingFace's free AI models to create
images from text descriptions. Features a modern Stable Diffusion-inspired
interface with 5 different AI models to choose from.

FEATURES
========
- 5 Free AI Models (FLUX.1, SDXL, Hyper-SD, Qwen, and more)
- Text-to-image generation
- Advanced controls (steps, guidance scale, negative prompts, seeds)
- Image gallery with download and copy features
- Dark/Light theme toggle
- 100% Free to use

TECH STACK
==========
- Backend: Python + Flask
- Frontend: HTML + CSS + Vanilla JavaScript
- API: HuggingFace Inference Providers

===============================================================================
HOW TO RUN
===============================================================================

STEP 1: GET HUGGINGFACE TOKEN (5 min)
--------------------------------------
1. Go to: https://huggingface.co/settings/tokens/new
2. Name: "Image Generator API"
3. Type: "Fine-grained"
4. Check: "Make calls to Inference Providers"
5. Click "Create token"
6. Copy your token (starts with hf_)

STEP 2: INSTALL DEPENDENCIES (2 min)
-------------------------------------
cd ai-image-generator-1/backend
python3 -m pip install Flask flask-cors huggingface-hub Pillow python-dotenv

STEP 3: ADD YOUR TOKEN (1 min)
-------------------------------
cd ai-image-generator-1/backend
cp .env.example .env
open -e .env  # or use any text editor

Replace:  HF_TOKEN=hf_your_token_here
With:     HF_TOKEN=hf_YourActualToken

Save and close.

STEP 4: START SERVER (30 sec)
------------------------------
cd ai-image-generator-1/backend
python3 app.py

You should see:
  * Running on http://127.0.0.1:5000
  * Services initialized successfully

STEP 5: OPEN IN BROWSER (10 sec)
---------------------------------
Navigate to: http://localhost:5000

STEP 6: GENERATE IMAGE (30 sec)
--------------------------------
1. Enter prompt: "A serene lake at sunset, photorealistic"
2. Click "Generate Image"
3. Wait 15-30 seconds
4. Done! 🎉

===============================================================================
TROUBLESHOOTING
===============================================================================

"No module named 'flask'"
→ Run: python3 -m pip install Flask flask-cors huggingface-hub Pillow python-dotenv

"HF_TOKEN is not set"
→ Make sure you created .env file and added your token

"Port 5000 already in use"
→ Stop other process or change PORT in .env to 5001

"Cannot access localhost:5000"
→ Check if server is running in terminal

"Image generation fails"
→ Verify token is correct and has "Inference Providers" permission

===============================================================================
PROJECT STRUCTURE
===============================================================================

ai-image-generator-1/
├── README.txt              # This file
├── QUICKSTART.txt          # Quick reference
├── backend/                # Python Flask API
│   ├── app.py             # Main server
│   ├── config.py          # Configuration
│   ├── requirements.txt   # Dependencies
│   ├── .env.example       # Environment template
│   ├── services/          # Business logic
│   ├── models/            # Model definitions
│   └── utils/             # Helper functions
└── frontend/               # Web interface
    ├── index.html         # Main page
    ├── css/style.css      # Styling
    └── js/                # JavaScript modules

===============================================================================
AVAILABLE MODELS
===============================================================================

1. FLUX.1 Dev        - Best quality, versatile (15-30s)
2. SDXL Lightning    - Fastest generation (5-10s)
3. Stable Diffusion XL - Most reliable (20-40s)
4. Hyper-SD          - Balanced speed/quality (10-20s)
5. Qwen Image        - Artistic styles (15-30s)

===============================================================================
TIPS FOR BEST RESULTS
===============================================================================

✓ Be specific and descriptive in prompts
✓ Use negative prompts to avoid unwanted elements
✓ Try guidance scale 7-8 for balanced results
✓ Higher steps = better quality (but slower)
✓ Use seeds to reproduce exact results

===============================================================================
STOPPING THE SERVER
===============================================================================

Press CTRL+C in the terminal where python3 app.py is running

To restart:
  cd ai-image-generator-1/backend
  python3 app.py

===============================================================================

Built with ❤️ using HuggingFace API, Flask, and Vanilla JavaScript
For educational purposes and learning Python web development

Last Updated: November 20, 2025
Version: 1.0.0

===============================================================================
