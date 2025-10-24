# Brand Moodboards

AI-powered word cloud generator for brand concepts using Google's Gemini API.

## Setup

1. **Add GitHub Secret:**
   - Go to Repository Settings → Secrets and variables → Actions
   - Add secret named `GEMINI_API_KEY` with your Gemini API key

2. **Enable GitHub Actions for Pages:**
   - Go to Repository Settings → Pages
   - Under "Build and deployment", select "GitHub Actions" as source

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

