# Rodin3D Skills

A Skill for generating 3D models from image/multiview images or text prompts using the Hyper3D Rodin Gen-2 API.

## Overview

This skill enables AI to generate high-quality 3D models through the Hyper3D Rodin Gen-2 API. It supports both image-to-3D and text-to-3D generation, with multiple output formats and quality tiers.

## Features

- Generate 3D models from single or multiple images (up to 5 images)
- Generate 3D models from text descriptions
- Support for multiple output formats: GLB, USDZ, FBX, OBJ, STL
- Five generation tiers: Gen-2, Detail, Smooth, Regular, Sketch
- Automatic task status polling and result retrieval
- Advanced parameters for material, mesh mode, seed values, and more

## Installation

### Prerequisites

- Hyper3D API Key (obtain from [https://hyper3d.ai/api-dashboard](https://hyper3d.ai/api-dashboard))
- Python 3.7+ (for backend scripts)

### Setup

1. Clone this repository
2. Install Python dependencies:

```bash
cd skills/rodin3d-skill
pip install -r requirements.txt
```

3. Set your Hyper3D API key as an environment variable:

```bash
export HYPER3D_API_KEY=your_api_key_here
```

Alternatively, create a `.env` file:

```bash
echo 'HYPER3D_API_KEY=your_api_key_here' > .env
echo '.env' >> .gitignore
```

4. Install the skill.

## Usage

### Using the Skill

Once installed, you can interact with this skill through:

**Generate from image:**
```
Please generate a 3D model from this image: [provide image path]
```

**Generate from text:**
```
Please generate a 3D model of a medieval castle with high quality
```

**Generate from multiple images:**
```
Please generate a 3D model from these images: [provide multiple images]
```

### Direct Script Usage

You can also use the Python scripts directly:

```bash
python scripts/generate_3d_model.py \
  --image path/to/image.jpg \
  --geometry-file-format glb \
  --quality medium \
  --output ./output
```

```bash
python scripts/generate_3d_model.py \
  --prompt "A detailed 3D model of a medieval castle" \
  --geometry-file-format glb \
  --quality high \
  --output ./output
```

## Configuration

### Generation Tiers

| Tier | Description | Use Case | Speed |
|------|-------------|----------|-------|
| Gen-2 | Highest quality, most advanced | Final production models | Slow |
| Detail | High detail, high resolution | Models requiring fine details | Medium |
| Smooth | Clear edges, smooth surface | Simple geometries, stylized models | Medium |
| Regular | Balanced quality and speed | General purpose | Medium |
| Sketch | Quick generation, low resolution | Concept validation, quick iteration | Fast |

### Output Formats

- GLB: Recommended for web and most 3D software
- USDZ: For Apple platforms
- FBX: For game engines and 3D modeling software
- OBJ: Universal 3D format
- STL: For 3D printing

### Quality Levels

- High: Best quality, longer processing time
- Medium: Balanced quality and speed
- Low: Faster processing, lower quality
- Extra-low: Fastest processing, minimal quality

## Parameters

### Basic Parameters

| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| `--image` | Input image path(s) (max 5) | File paths | - |
| `--prompt` | Text prompt for generation | Text | - |
| `--tier` | Generation tier | Gen-2, Detail, Smooth, Regular, Sketch | Gen-2 |
| `--geometry-file-format` | Output format | glb, usdz, fbx, obj, stl | glb |
| `--quality` | Quality level | high, medium, low, extra-low | medium |
| `--output` | Output directory | Directory path | - |

### Advanced Parameters

| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| `--material` | Material type | PBR, Shaded, All | PBR |
| `--mesh-mode` | Mesh topology | Raw, Quad | Quad |
| `--use-original-alpha` | Use original alpha channel | - | False |
| `--seed` | Random seed value | 0-65535 | - |
| `--quality-override` | Custom polygon count | Integer | - |
| `--tapose` | Generate T/A pose | - | False |
| `--bbox-condition` | Bounding box [W, H, L] | Three integers | - |
| `--addons` | Additional features | HighPack | - |
| `--preview-render` | Generate preview render | - | False |
| `--poll-interval` | Status check interval (seconds) | Integer | 10 |
| `--max-retries` | Maximum retry attempts | Integer | 60 |

## Best Practices

### Image Input

- Use high-resolution images (at least 512 x 512 pixels)
- Ensure good lighting and clear details
- Avoid cluttered backgrounds
- Use multiple angles for better results
- Supported formats: JPEG, PNG, WEBP
- File size limit: 16MB
- Resolution range: 512x512 to 4096x4096

### Text Prompts

- Be specific and detailed in your descriptions
- Mention materials and textures
- Include lighting information
- Specify the style (realistic, cartoon, futuristic, etc.)
- Provide context for the object

### Important Notes

**Download links expire in 10 minutes**: API result URLs are temporary. Download 3D models immediately after generation completes. Do not store or cache the URLs themselves.

## Project Structure

```
rodin3d-skills-git/
├── skills/
│   └── rodin3d-skill/
│       ├── SKILL.md                 # Skill documentation
│       ├── requirements.txt         # Python dependencies
│       ├── assets/
│       │   └── examples/
│       │       └── README.md        # Example documentation
│       └── scripts/
│           ├── api_client.py        # API client implementation
│           ├── generate_3d_model.py # Main generation script
│           └── image_utils.py       # Image processing utilities
└── README.md                        # This file
```

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `https://api.hyper3d.com/api/v2/rodin` | Submit 3D model generation task |
| `https://api.hyper3d.com/api/v2/status` | Check task status |
| `https://api.hyper3d.com/api/v2/download` | Get download links for completed tasks |

## Example Prompts

Here are some example text prompts for 3D generation:

1. "A detailed 3D model of a medieval castle"
2. "A futuristic cityscape with flying cars"
3. "A realistic 3D model of a cat sitting on a couch"
4. "An abstract sculpture made of glass and metal"
5. "A 3D model of a cozy cottage in the woods"

## Troubleshooting

### API Key Issues

If you encounter authentication errors:
1. Verify your API key is set correctly
2. Check that the key is valid and active
3. Ensure you have sufficient API credits

### Generation Failures

If generation fails:
1. Check image format and size requirements
2. Verify prompt is not empty or too short
3. Ensure API service is available
4. Review error messages for specific issues

## Documentation

For detailed documentation, see:
- [SKILL.md](skills/rodin3d-skill/SKILL.md) - Complete skill documentation
- [assets/examples/README.md](skills/rodin3d-skill/assets/examples/README.md) - Example usage

## Links

- [Hyper3D Website](https://hyper3d.ai)
- [API Dashboard](https://hyper3d.ai/api-dashboard)
- [Hyper3D API Documentation](https://developer.hyper3d.ai/)

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Submit a GitHub Issue
- Refer to [SKILL.md](skills/rodin3d-skill/SKILL.md) for detailed documentation
- Visit Hyper3D official documentation

---

Author: HyperHuman  
Version: 1.0.0  
Tags: 3D Asset, Hyper3D, Rodin Gen-2, API, 3D Model, Image-to-3D, Text-to-3D