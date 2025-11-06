#!/usr/bin/env python3
"""
Generate images for Story 4 positioning slides using Gemini 2.5 Flash Image
"""
import os
import requests
import json
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Image descriptions - simple photographic compositions
# 16:9 aspect ratio, naturally out-of-focus top areas
IMAGE_PROMPTS = [
    {
        "slide": 1,
        "name": "foundation",
        "prompt": "Photograph of massive concrete foundation pillars underground, shot from below looking up, warm golden light filtering from above, the top third of frame naturally out of focus creating a warm light background",
        "text_color": "white"
    },
    {
        "slide": 2,
        "name": "ladder_to_moon",
        "prompt": "Photograph of a wooden ladder reaching toward a full moon in a dark evening sky, ladder in lower half of frame, upper portion is smooth dark blue night sky gradually fading darker toward top",
        "text_color": "white"
    },
    {
        "slide": 3,
        "name": "integration",
        "prompt": "Photograph of hands manipulating laboratory glassware with AR glasses, shot with shallow depth of field, the background at top naturally blurred into soft light tones",
        "text_color": "black"
    },
    {
        "slide": 4,
        "name": "two_tracks",
        "prompt": "Aerial photograph of parallel railway tracks extending toward distant mountains at golden hour, tracks in lower two-thirds, warm golden sky gradually lightening toward top of frame",
        "text_color": "black"
    },
    {
        "slide": 5,
        "name": "unlocking",
        "prompt": "Photograph of an ornate brass key in an antique lock, tight focus on the key mechanism in lower portion, background naturally blurred to soft warm tones toward top",
        "text_color": "black"
    }
]

def generate_image(prompt, output_path):
    """Generate image using Gemini 2.5 Flash Image API"""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
    
    # Clean prompt - no text or graphics
    full_prompt = f"{prompt}. Professional photography, no text or graphics."
    
    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generation_config": {
            "image_config": {
                "aspect_ratio": "16:9"
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Generating: {output_path.name}...")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False
    
    data = response.json()
    
    # Extract image data from response
    if 'candidates' in data and len(data['candidates']) > 0:
        parts = data['candidates'][0]['content']['parts']
        
        # Find the inlineData part with the image
        for part in parts:
            if 'inlineData' in part:
                image_data = part['inlineData']['data']
                
                # Decode base64 and save as PNG
                image_bytes = base64.b64decode(image_data)
                with open(output_path, 'wb') as f:
                    f.write(image_bytes)
                
                print(f"✓ Image saved to {output_path}")
                return True
        
        print(f"✗ No image data found in response")
        return False
    else:
        print(f"✗ No candidates in response")
        return False

def main():
    # Create output directory
    output_dir = Path(__file__).parent / "images"
    output_dir.mkdir(exist_ok=True)
    
    print(f"Generating {len(IMAGE_PROMPTS)} images for Story 4...")
    print(f"Output directory: {output_dir}")
    print()
    
    # Also save text color information
    text_colors = {}
    for item in IMAGE_PROMPTS:
        output_path = output_dir / f"slide_{item['slide']}_{item['name']}.png"
        generate_image(item['prompt'], output_path)
        text_colors[item['slide']] = item['text_color']
        print()
    
    # Save text color mapping
    import json
    with open(output_dir / "text_colors.json", 'w') as f:
        json.dump(text_colors, f, indent=2)
    print(f"✓ Text colors saved to text_colors.json")
    
    print("Done!")

if __name__ == "__main__":
    main()

