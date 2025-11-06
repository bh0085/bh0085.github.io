# Positioning Slides - Image Generation

This directory contains the positioning slides presentation and tools for generating AI-powered background images.

## Overview

The project includes 4 story presentations:
- **Story 1**: The Scientific Infrastructure - Building the operating system for automated science
- **Story 2**: The Data Differentiation - Unlocking breakthroughs through operational data
- **Story 3**: The Company vs. Product - We're building a platform company, not a single product
- **Story 4**: The Ladder to the Moon - Operational superintelligence is the necessary foundation

Each story has 5 slides with compelling topic sentences and beautiful matched imagery.

## Image Generation

### Setup

1. Install required dependencies:
```bash
pip install -r ../requirements.txt
```

2. Create a `.env` file in the project root with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

### Usage

The `generate_images.py` script uses Google's Gemini 2.5 Flash Image API to generate professional photography-style background images for each slide.

**Generate all images for all stories:**
```bash
python3 generate_images.py
```

**Generate all images for a specific story:**
```bash
python3 generate_images.py --story 1  # Story 1
python3 generate_images.py --story 2  # Story 2
python3 generate_images.py --story 3  # Story 3
python3 generate_images.py --story 4  # Story 4
```

**Regenerate specific slides within a story:**
```bash
python3 generate_images.py --story 1 --slide 2        # Regenerate only slide 2 of story 1
python3 generate_images.py --story 3 --slide 1 3 5    # Regenerate slides 1, 3, and 5 of story 3
```

### Image Specifications

- **Aspect Ratio**: 16:9 (optimized for presentation displays)
- **Format**: PNG
- **Composition**: Professional photography with naturally out-of-focus top area for text overlay
- **Text Colors**: Automatically determined (light backgrounds = black text, dark backgrounds = white text)

### Output

Images are saved in the `images/` directory with the naming convention:
```
story{N}_slide_{M}_{name}.png
```

For example:
- `story1_slide_1_operating_system.png`
- `story2_slide_3_data_moat.png`
- `story4_slide_2_ladder_to_moon.png`

Text color information is saved in `images/text_colors.json` for use by the presentation HTML files.

## Slide Content

### Story 1: The Scientific Infrastructure
1. **Operating System** - We're building the operating system for automated science
2. **Bottleneck** - Current scientific work is bottlenecked by manual, inconsistent human operations
3. **Unified Platform** - Our first product, LabOS, is a unified platform integrating perception, intelligence, and action
4. **Rapid Expansion** - Our core platform architecture is designed for rapid expansion into new scientific domains
5. **One Platform** - From lab automation to clinical trials and beyond—one platform, many applications

### Story 2: The Data Differentiation
1. **Operational Data** - We generate the operational data that AI needs but cannot access
2. **Starved for Data** - The AI revolution is starved for the physical-world data that drives scientific discovery
3. **Data Moat** - Our XR and robotics platform creates a proprietary, compounding data moat over time
4. **Data Engines** - Our first products, LabOS and ClinOS, are engines for generating this unique operational data
5. **Compounding Advantage** - Every experiment captured, every protocol learned, every deployment compounds our data advantage

### Story 3: The Company vs. Product
1. **Platform Company** - We're a platform company that builds multiple products, not a single-product company
2. **Tracks Framework** - Our 'tracks' framework signals a broad, scalable vision beyond any single application
3. **Shared Platform** - A shared platform architecture allows us to serve distinct markets while reusing core technology
4. **Network Effects** - Learnings and data from each track create compounding network effects across the entire platform
5. **Building Company** - One platform, multiple tracks, compounding advantages—we're building the company that automates science

### Story 4: The Ladder to the Moon
1. **Foundation** - Embodied AI is the necessary foundation for scientific superintelligence
2. **Ladder to Moon** - Purely computational AI approaches are insufficient for true scientific breakthroughs
3. **Integration** - We uniquely combine sensory perception, AI reasoning, and physical action
4. **Two Tracks** - Our two initial product tracks validate the platform and build towards our long-term vision
5. **Unlocking** - Better sensors, not just better models—operational superintelligence unlocks scientific superintelligence

## Presentation Files

- `story1.html` - Story 1 presentation
- `story2.html` - Story 2 presentation
- `story3.html` - Story 3 presentation
- `story4.html` - Story 4 presentation
- `index.html` - Landing page for all stories
- `summary.html` - Summary view of all stories
- `nav.js` - Navigation component shared across all presentations

## Features

- 📱 Responsive design (mobile, tablet, desktop)
- ⌨️ Keyboard navigation (arrow keys)
- 🖼️ Fullscreen presentation mode
- 🎨 Beautiful background images with professional photography
- 🎯 Strong, compelling topic sentences
- ⚡ Fast image preloading
- 🔄 Smooth transitions between slides

