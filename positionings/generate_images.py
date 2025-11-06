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

# Image descriptions from story4.html
IMAGE_PROMPTS = [
    {
        "slide": 1,
        "name": "foundation",
        "prompt": "Deep concrete foundation pillars being constructed underground, photographed from below looking upward, showing massive structural support beams in warm afternoon light filtering from above, emphasizing strength and permanence"
    },
    {
        "slide": 2,
        "name": "ladder_to_moon",
        "prompt": "A tall wooden ladder leaning against an evening sky, reaching upward but clearly falling short of the glowing full moon visible high above, vast empty space between ladder top and moon, emphasizing the impossible gap"
    },
    {
        "slide": 3,
        "name": "integration",
        "prompt": "Close-up of precise human hands carefully manipulating delicate laboratory glassware while wearing sleek AR glasses that reflect data, soft natural window light from the side, shallow depth of field focusing on the fusion of seeing, thinking, and doing"
    },
    {
        "slide": 4,
        "name": "two_tracks",
        "prompt": "Aerial view of two parallel railway tracks stretching into the distance toward a majestic mountain range at golden hour, strong converging perspective drawing the eye forward to the distant peaks, warm sunlight on the rails"
    },
    {
        "slide": 5,
        "name": "unlocking",
        "prompt": "A brass skeleton key being inserted into an ornate antique lock mechanism in sharp focus, soft bokeh background, warm directional lighting catching the metallic surfaces, capturing the precise moment before unlocking and breakthrough"
    }
]

def generate_image(prompt, output_path):
    """Generate image using Gemini 2.5 Flash Image API"""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
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
    
    for item in IMAGE_PROMPTS:
        output_path = output_dir / f"slide_{item['slide']}_{item['name']}.png"
        generate_image(item['prompt'], output_path)
        print()
    
    print("Done!")

if __name__ == "__main__":
    main()

