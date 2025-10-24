# Brand Moodboards

AI-powered word cloud generator for brand concepts using Google's Gemini API.

## Setup - Configure API Key

The API key is already in the code, but needs to be configured in Google Cloud Console:

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/apis/credentials
   - Find your API key: `AIzaSyBPwwjrvnUhTqmjF2i-pcnMsRq8ZreLGjU`

2. **Add HTTP Referrer Restrictions:**
   - Click on the API key to edit it
   - Under "Application restrictions", select "HTTP referrers (web sites)"
   - Click "Add an item" and add:
     - `https://www.mlcl.ai/*`
     - `https://mlcl.ai/*`
   - Save the changes

3. **Wait ~1 minute for changes to propagate**

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

