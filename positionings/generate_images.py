#!/usr/bin/env python3
"""
Generate images for positioning slides using Gemini 2.5 Flash Image

Usage:
  python3 generate_images.py                    # Generate all slides for all stories
  python3 generate_images.py --story 1          # Generate all slides for story 1
  python3 generate_images.py --story 1 --slide 2  # Regenerate only story 1, slide 2
  python3 generate_images.py --story 4 --slide 1 3 5  # Regenerate story 4, slides 1, 3, and 5
"""
import os
import sys
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

# Image prompts for all stories - simple photographic compositions with 16:9 aspect ratio
# Each has naturally out-of-focus top area for text overlay
IMAGE_PROMPTS = {
    1: {  # Story 1: The Scientific Infrastructure
        "name": "The Scientific Infrastructure",
        "slides": [
            {
                "slide": 1,
                "name": "operating_system",
                "background": "light",
                "prompt": (
                    "Overhead aerial photograph of a massive modern data center or server farm, "
                    "clean geometric white and silver architecture, organized in precise grids, "
                    "bright open sky at top of frame, the upper third naturally light and minimal "
                    "for clean composition, professional architectural photography"
                )
            },
            {
                "slide": 2,
                "name": "bottleneck",
                "background": "light",
                "prompt": (
                    "Photograph of a scientist's hands manually pipetting in a cluttered traditional "
                    "laboratory, repetitive lab equipment visible, warm fluorescent lighting, shot from "
                    "above with shallow depth of field, upper portion naturally blurred into soft tones, "
                    "conveying manual tedious work"
                )
            },
            {
                "slide": 3,
                "name": "unified_platform",
                "background": "light",
                "prompt": (
                    "Photograph of a sleek modern laboratory automation system, robotic arms and "
                    "precision instruments working together, clean white and chrome surfaces, "
                    "blue LED accent lighting, shot at an angle showing integration of multiple "
                    "components, upper area naturally fading to bright clean background"
                )
            },
            {
                "slide": 4,
                "name": "rapid_expansion",
                "background": "light",
                "prompt": (
                    "Photograph of interconnected modular building blocks or LEGO-like structures "
                    "expanding outward, white and translucent materials, each module containing "
                    "miniature scientific equipment visible inside, natural lighting from above "
                    "creating bright upper frame, conveying scalable modular architecture"
                )
            },
            {
                "slide": 5,
                "name": "one_platform",
                "background": "light",
                "prompt": (
                    "Wide aerial photograph of a sprawling futuristic research campus or technology "
                    "park with multiple connected buildings, clean modernist architecture, green "
                    "courtyards, unified design language, bright sky gradient at top third, "
                    "conveying unified ecosystem and broad vision"
                )
            }
        ]
    },
    2: {  # Story 2: The Data Differentiation
        "name": "The Data Differentiation",
        "slides": [
            {
                "slide": 1,
                "name": "operational_data",
                "background": "dark",
                "prompt": (
                    "Photograph of a laboratory microscope with holographic data visualizations "
                    "floating above it, streams of glowing blue and green data particles rising "
                    "upward, dark background, upper portion dark blue to black gradient, "
                    "conveying generation of unique digital data from physical processes"
                )
            },
            {
                "slide": 2,
                "name": "starved_for_data",
                "background": "dark",
                "prompt": (
                    "Photograph of a barren cracked earth landscape at dusk, single small seedling "
                    "emerging from dry ground, deep blue evening sky gradually darkening toward top, "
                    "dramatic lighting on the seedling, conveying scarcity and need"
                )
            },
            {
                "slide": 3,
                "name": "data_moat",
                "background": "light",
                "prompt": (
                    "Aerial photograph of a massive modern dam or reservoir with crystalline blue "
                    "water, sleek concrete architecture, water flowing and accumulating, mountains "
                    "in background, bright sky at top third, conveying accumulation and "
                    "compounding strategic advantage"
                )
            },
            {
                "slide": 4,
                "name": "data_engines",
                "background": "light",
                "prompt": (
                    "Photograph of precision laboratory equipment capturing a chemical reaction, "
                    "high-speed camera with visible sensors, holographic overlay showing data "
                    "capture, clean modern aesthetic with blue and white tones, upper area "
                    "naturally bright, conveying active data generation"
                )
            },
            {
                "slide": 5,
                "name": "compounding_advantage",
                "background": "light",
                "prompt": (
                    "Photograph of a geometric spiral or fibonacci pattern in nature, like a nautilus "
                    "shell cross-section or unfurling fern, clean white background with natural "
                    "lighting from above, upper area bright and minimal, conveying organic growth "
                    "and compounding effects"
                )
            }
        ]
    },
    3: {  # Story 3: The Company vs. Product
        "name": "The Company vs. Product",
        "slides": [
            {
                "slide": 1,
                "name": "platform_company",
                "background": "light",
                "prompt": (
                    "Aerial photograph of a massive modern industrial complex or technology campus "
                    "with multiple distinct buildings connected by walkways, unified architectural "
                    "style, white and glass structures, organized layout showing multiple sectors, "
                    "bright sky at top, conveying multi-product platform ecosystem"
                )
            },
            {
                "slide": 2,
                "name": "tracks_framework",
                "background": "light",
                "prompt": (
                    "Aerial photograph of multiple parallel railway tracks branching from a central "
                    "hub or junction, clean modern rail infrastructure, tracks extending in different "
                    "directions toward the horizon, golden hour lighting, bright sky gradient at top, "
                    "conveying multiple paths from single source"
                )
            },
            {
                "slide": 3,
                "name": "shared_platform",
                "background": "light",
                "prompt": (
                    "Photograph of a modular construction system showing a central platform or "
                    "foundation with different specialized modules connecting to it, clean industrial "
                    "design, white and metallic materials, organized layout, natural lighting from "
                    "above, conveying shared infrastructure with diverse applications"
                )
            },
            {
                "slide": 4,
                "name": "network_effects",
                "background": "light",
                "prompt": (
                    "Photograph of interconnected neural network or mycelium structure, organic "
                    "branching patterns glowing with subtle blue light, nodes connecting and "
                    "strengthening each other, white or light background, upper area naturally "
                    "bright, conveying interconnection and compounding benefits"
                )
            },
            {
                "slide": 5,
                "name": "building_company",
                "background": "light",
                "prompt": (
                    "Wide aerial photograph of a gleaming modern research and development campus "
                    "under construction, multiple buildings at different stages, unified vision "
                    "visible, construction cranes suggesting growth, mountains or landscape in "
                    "background, bright gradient sky at top, conveying ambitious company building"
                )
            }
        ]
    },
    4: {  # Story 4: The Ladder to the Moon
        "name": "The Ladder to the Moon",
        "slides": [
            {
                "slide": 1,
                "name": "foundation",
                "background": "light",
                "prompt": (
                    "Overhead aerial photograph of a massive futuristic concrete spaceport "
                    "under construction, clean modernist architecture, white and light gray "
                    "concrete structures, bright sky at top of frame, the upper third naturally "
                    "light and minimal for clean composition"
                )
            },
            {
                "slide": 2,
                "name": "ladder_to_moon",
                "background": "dark",
                "prompt": (
                    "Photograph of a wooden ladder reaching toward a full moon in a dark "
                    "evening sky, ladder in lower half of frame, upper portion is smooth "
                    "dark blue night sky gradually fading darker toward top"
                )
            },
            {
                "slide": 3,
                "name": "integration",
                "background": "light",
                "prompt": (
                    "Photograph of hands manipulating laboratory glassware with AR glasses, "
                    "shot with shallow depth of field, the background at top naturally blurred "
                    "into soft light tones"
                )
            },
            {
                "slide": 4,
                "name": "two_tracks",
                "background": "light",
                "prompt": (
                    "Aerial photograph of parallel railway tracks extending toward distant "
                    "mountains at golden hour, tracks in lower two-thirds, warm golden sky "
                    "gradually lightening toward top of frame"
                )
            },
            {
                "slide": 5,
                "name": "unlocking",
                "background": "light",
                "prompt": (
                    "Photograph of an ornate brass key in an antique lock, tight focus on "
                    "the key mechanism in lower portion, background naturally blurred to "
                    "soft warm tones toward top"
                )
            }
        ]
    }
}

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
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate images for positioning slides')
    parser.add_argument('--story', type=int, choices=[1, 2, 3, 4], 
                       help='Story number to generate (1-4). If omitted, generates all stories.')
    parser.add_argument('--slide', type=int, nargs='+', 
                       help='Specific slide number(s) to regenerate (1-5). Only works with --story.')
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(__file__).parent / "images"
    output_dir.mkdir(exist_ok=True)
    
    # Determine which stories and slides to generate
    if args.story:
        stories_to_generate = [args.story]
        if args.slide:
            print(f"Regenerating Story {args.story}, slides: {', '.join(map(str, args.slide))}")
        else:
            print(f"Generating all slides for Story {args.story}: {IMAGE_PROMPTS[args.story]['name']}")
    else:
        if args.slide:
            print("Error: --slide requires --story to be specified")
            sys.exit(1)
        stories_to_generate = [1, 2, 3, 4]
        print("Generating all slides for all stories")
    
    print(f"Output directory: {output_dir}")
    print()
    
    # Track text colors for all generated slides
    # Load existing colors if any
    colors_file = output_dir / "text_colors.json"
    if colors_file.exists():
        with open(colors_file, 'r') as f:
            text_colors = json.load(f)
    else:
        text_colors = {}
    
    # Generate images
    total_generated = 0
    for story_num in stories_to_generate:
        story_data = IMAGE_PROMPTS[story_num]
        print(f"=== Story {story_num}: {story_data['name']} ===")
        
        # Determine which slides to generate for this story
        if args.story == story_num and args.slide:
            slides_to_gen = [s for s in story_data['slides'] if s['slide'] in args.slide]
        else:
            slides_to_gen = story_data['slides']
        
        for slide_data in slides_to_gen:
            slide_num = slide_data['slide']
            output_path = output_dir / f"story{story_num}_slide_{slide_num}_{slide_data['name']}.png"
            
            print(f"Story {story_num}, Slide {slide_num}: {slide_data['name']}")
            success = generate_image(slide_data['prompt'], output_path)
            
            if success:
                # Store text color (format: "story_slide")
                color_key = f"{story_num}_{slide_num}"
                text_colors[color_key] = "white" if slide_data['background'] == "dark" else "black"
                total_generated += 1
            
            print()
        
        print()
    
    # Save text color mapping
    with open(colors_file, 'w') as f:
        json.dump(text_colors, f, indent=2, sort_keys=True)
    print(f"✓ Text colors saved to text_colors.json")
    print(f"✓ Generated {total_generated} images")
    print("Done!")

if __name__ == "__main__":
    main()

