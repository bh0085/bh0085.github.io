# Brand Moodboards

AI-powered word cloud generator for brand concepts using Google's Gemini API.

## Setup - Enable the API

The API key is in the code, but the **Generative Language API needs to be enabled**:

### Step 1: Enable the Generative Language API

1. **Go to API Library:**
   - Visit: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
   
2. **Click "ENABLE"** button

3. **Wait ~1 minute** for activation

### Step 2 (Optional): Add Referrer Restrictions for Security

1. **Go to Credentials:**
   - Visit: https://console.cloud.google.com/apis/credentials
   
2. **Edit your API key:**
   - Find: `GEMINI_API_KEY_PLACEHOLDER`
   - Click to edit
   
3. **Add HTTP Referrer Restrictions:**
   - Under "Application restrictions", select "HTTP referrers (web sites)"
   - Add items:
     - `https://www.mlcl.ai/*`
     - `https://mlcl.ai/*`
   - Save

## How It Works

- Click any concept card to generate a poetic word cloud
- The Gemini API generates 30-40 evocative words related to the concept
- Words are displayed with random sizes and opacity for visual effect
- No backend server required - runs entirely client-side
- API key is injected securely at build time via GitHub Actions

## Concepts

- **Vision Catalyst**: Perception-driven evolution
- **Emergent Intelligence**: Grown, not programmed  
- **Dimensional Discovery**: Spatial understanding
- **Cambrian Moment**: Vision changes everything
- **Symbiotic Intelligence**: Human + AI co-evolution
- **Pattern Acceleration**: Compressed evolution

## Technical Details

Based on the genai API call pattern from the studio benchling ingestion code:
- Direct REST API calls to Google's Generative Language API
- Uses `gemini-2.0-flash-exp` model for fast responses
- Mobile-responsive design with Tailwind CSS

