---
name: rodin3d-skill
description: Enterprise-grade 3D model generation using Hyper3D Rodin Gen-2.5 API. Enables production-quality Image-to-3D and Text-to-3D conversion with advanced geometry and texture controls.
metadata:
  author: HyperHuman
  version: "2.0.0"
  tags: 3D Asset, Hyper3D, Rodin, Rodin Gen-2.5, API, 3D Model, Image-to-3D, Text-to-3D, AI Generation
  documentation: https://developer.hyper3d.ai/api-specification/rodin-gen2.5
---

# Hyper3D Rodin Gen-2.5 Skill Documentation

## Overview

This skill provides a comprehensive integration with the **Hyper3D Rodin Gen-2.5 API**, enabling developers to generate production-ready 3D models from images or text prompts. The skill handles API authentication, task submission, status polling, and result retrieval with enterprise-grade reliability.

**Key Capabilities:**
- Image-to-3D reconstruction (up to 5 input images)
- Text-to-3D generation
- Advanced geometry and texture controls
- Multi-format output support (glb, usdz, fbx, obj, stl)
- Asynchronous task management with automatic polling

## Quick Start

### Prerequisites
1. **API Key**: 
   - **Free Test Key**: `vibecoding` (automatically used when no key is provided)
   - **Production Key**: Obtain from [Hyper3D API Dashboard](https://hyper3d.ai/api-dashboard)
2. **Python 3.8+**
3. **Dependencies**: Install via `pip install -r requirements.txt`

### Basic Usage

```bash
# Quick start with free test key (no API key required)
python scripts/generate_3d_model.py \
  --image input.jpg \
  --tier Gen-2.5-Medium \
  --output ./output

# Generate from image with your API key
python scripts/generate_3d_model.py \
  --image input.jpg \
  --tier Gen-2.5-High \
  --geometry-file-format glb \
  --quality medium \
  --output ./output \
  --api-key $HYPER3D_API_KEY

# Generate from text
python scripts/generate_3d_model.py \
  --prompt "A detailed 3D model of a vintage camera" \
  --tier Gen-2.5-Medium \
  --output ./output
```

## Core Concepts

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v2/rodin` | POST | Submit generation task |
| `/api/v2/status` | POST | Check task status |
| `/api/v2/download` | POST | Retrieve download links |

### Task Lifecycle

1. **Submit**: POST to `/api/v2/rodin` → Returns `subscription_key` and `task_uuid`
2. **Poll**: POST to `/api/v2/status` with `subscription_key` → Check job status
3. **Download**: POST to `/api/v2/download` with `task_uuid` → Get result URLs (expire in 10 minutes)

## Parameter Reference

### Tier Selection

| Tier | Description | Credit Cost | Recommended Use Case |
|------|-------------|-------------|---------------------|
| `Gen-2.5-Extreme-Low` | Rapid generation for simple assets | 0.5 | Prototyping, quick iterations |
| `Gen-2.5-Low` | Clean assets, small hardsurface props | 0.5 | Basic models, low-poly assets |
| `Gen-2.5-Medium` | Balanced structure and detail | 0.5 | **Default** - general purpose |
| `Gen-2.5-High` | Rich structural representation, smooth surfaces | 0.5 | Production-ready assets |
| `Gen-2.5-Extreme-High` | High-frequency detail reproduction | 1.0 | Premium quality, final renders |
| `Gen-2` | Legacy tier | 0.5 | Backward compatibility |
| `Detail/Regular/Smooth/Sketch` | Legacy tiers | 0.5 | Deprecated, use Gen-2.5 |

### Quality Levels (Face Count)

| Quality | Raw Mode | Quad Mode | Use Case |
|---------|----------|-----------|----------|
| `high` | 1M faces | 50k faces | Production, close-ups |
| `medium` | 500k faces | 18k faces | **Default** - balanced |
| `low` | 60k faces | 8k faces | Real-time applications |
| `extra-low` | 20k faces | 4k faces | Mobile, VR/AR |

### Material Types

| Material | Description |
|----------|-------------|
| `PBR` | Physically Based Rendering (base color, metallic, normal, roughness maps) |
| `Shaded` | Base color texture with baked lighting |
| `All` | Both PBR and Shaded materials |
| `None` | Geometry only, no materials |

### Gen-2.5 Exclusive Features

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `hd_texture` | bool | Enable 4K texture generation | false |
| `texture_delight` | bool | Enhance texture quality and detail | false |
| `texture_mode` | string | Advanced texture generation mode | None |
| `is_micro` | bool | Optimize for micro-scale objects | false |
| `geometry_instruct_mode` | string | Geometry generation guidance | `faithful` |

### Mesh Mode Comparison

| Mode | Description | Recommended For |
|------|-------------|----------------|
| `Raw` | Triangle mesh, maximum detail preservation | Gen-2.5 tiers |
| `Quad` | Quadrilateral mesh, cleaner topology | Legacy tiers |

### Addons

| Addon | Cost | Description |
|-------|------|-------------|
| `HighPack` | +1 credit | 4K texture resolution upgrade |

## Command Line Interface

### Required Arguments

```bash
# Image input (required for Image-to-3D)
--image path/to/image1.jpg [path/to/image2.jpg ...]

# OR Text input (required for Text-to-3D)
--prompt "Your text description"
```

### Optional Arguments

```bash
# Core settings
--tier Gen-2.5-Medium              # Generation tier
--geometry-file-format glb          # Output format: glb, usdz, fbx, obj, stl
--quality medium                    # Face count: high, medium, low, extra-low
--material PBR                      # Material type: PBR, Shaded, All

# Advanced geometry
--mesh-mode Raw                     # Raw or Quad
--quality-override 500000          # Custom polygon count
--bbox-condition 100 100 100       # Bounding box [Width, Height, Length]
--tapose                           # Generate T/A pose for humanoids

# Texture enhancements (Gen-2.5)
--hd-texture                       # Enable HD textures
--texture-delight                  # Enhance texture quality
--texture-mode <mode>              # Advanced texture mode

# Object properties (Gen-2.5)
--is-micro                         # Micro-scale optimization

# Generation control
--seed 12345                       # Random seed (0-65535)
--geometry-instruct-mode faithful  # Geometry guidance mode

# Output options
--preview-render                   # Generate preview image
--addons HighPack                  # Additional features
--output ./output                  # Download directory
--api-key $HYPER3D_API_KEY         # Authentication

# Polling configuration
--poll-interval 10                 # Status check interval (seconds)
--max-retries 60                   # Maximum polling attempts
```

## Usage Recipes

### Recipe 1: Production-Quality Asset

```bash
python scripts/generate_3d_model.py \
  --image product.jpg \
  --tier Gen-2.5-High \
  --geometry-file-format glb \
  --quality high \
  --material PBR \
  --mesh-mode Raw \
  --hd-texture \
  --texture-delight \
  --addons HighPack \
  --output ./production
```

### Recipe 2: Rapid Prototyping

```bash
python scripts/generate_3d_model.py \
  --prompt "A futuristic smartphone" \
  --tier Gen-2.5-Extreme-Low \
  --geometry-file-format glb \
  --quality low \
  --output ./prototypes
```

### Recipe 3: Fast Generation Mode

Fast generation mode is triggered by a specific combination of parameters optimized for speed:

```bash
python scripts/generate_3d_model.py \
  --image product.jpg \
  --tier Gen-2.5-Low \
  --material Shaded \
  --mesh-mode Raw \
  --quality-override 20000 \
  --texture-mode low \
  --output ./quick-preview
```

**Fast Mode Parameters:**

| Parameter | Value | Description |
|-----------|-------|-------------|
| `tier` | `Gen-2.5-Low` | Use low tier for faster generation |
| `material` | `Shaded` | Simplified material output |
| `mesh_mode` | `Raw` | Triangle mesh for faster processing |
| `quality_override` | `20000` | Reduced polygon count |
| `texture_mode` | `low` | Low resolution textures |

**Trigger Condition:** Fast mode is automatically activated when all of the above parameters are set together. This combination provides the quickest generation time for rapid prototyping and preview purposes.

### Recipe 4: Batch Processing Workflow

```bash
# Process multiple images sequentially
for img in ./input/*.jpg; do
  python scripts/generate_3d_model.py \
    --image "$img" \
    --tier Gen-2.5-Medium \
    --output ./output/$(basename "$img" .jpg)
done
```

## Python API Integration

### Basic Client Usage

```python
from api_client import Hyper3DAPIClient

# Initialize client
client = Hyper3DAPIClient(api_key="your_api_key")

# Generate from image
task_uuid, result = client.generate_3d_model(
    images=["input.jpg"],
    tier="Gen-2.5-High",
    geometry_file_format="glb",
    quality="high",
    material="PBR",
    mesh_mode="Raw",
    hd_texture=True,
    texture_delight=True,
    poll_interval=15,
    max_retries=40
)

# Process results
print(f"Task completed: {task_uuid}")
for file_info in result.get("list", []):
    print(f"File: {file_info['name']} - URL: {file_info['url']}")
```

### Advanced Configuration

```python
from api_client import Hyper3DAPIClient

client = Hyper3DAPIClient(api_key="your_api_key")

# Custom generation with all parameters
task_uuid, result = client.generate_3d_model(
    images=["front.jpg", "side.jpg", "top.jpg"],
    prompt="A vintage pocket watch with intricate details",
    tier="Gen-2.5-Extreme-High",
    geometry_file_format="fbx",
    quality="high",
    material="All",
    mesh_mode="Raw",
    use_original_alpha=True,
    seed=42,
    TAPose=False,
    bbox_condition=[100, 100, 50],
    addons=["HighPack"],
    preview_render=True,
    hd_texture=True,
    texture_delight=True,
    is_micro=False,

    geometry_instruct_mode="faithful"
)
```

### Manual Task Management

```python
# Submit task
submit_result = client.submit_generation_task(
    images=["input.jpg"],
    tier="Gen-2.5-Medium"
)

subscription_key = submit_result["jobs"]["subscription_key"]
task_uuid = submit_result["uuid"]

# Manual polling
import time
for _ in range(60):
    status = client.check_task_status(subscription_key)
    jobs = status.get("jobs", [])
    
    if all(job["status"] == "Done" for job in jobs):
        break
    elif any(job["status"] == "Failed" for job in jobs):
        raise Exception("Task failed")
    
    time.sleep(10)

# Get download links
download_result = client.download_results(task_uuid)
```

## Error Handling & Troubleshooting

### Common Error Codes

| Error | Cause | Resolution |
|-------|-------|------------|
| `Not authenticated` | Invalid or missing API key | Verify `HYPER3D_API_KEY` is set correctly |
| `INSUFFICIENT_FUND` | Insufficient credits | Add funds via Hyper3D dashboard |
| `Invalid tier` | Unknown tier value | Use valid Gen-2.5 tier (see Tier Selection) |
| `Invalid image` | Image format/size error | Use JPEG/PNG/WebP, max 16MB, 512x512-4096x4096 |
| `Timeout` | Generation took too long | Increase `--max-retries`, check API status |

### Best Practices

1. **Validate Inputs**: Use `ImageUtils.validate_image()` before submission
2. **Handle Rate Limits**: Implement exponential backoff for retries
3. **Store Results**: Download models immediately - URLs expire in 10 minutes
4. **Log Everything**: Track task UUIDs and status for debugging
5. **Use Appropriate Tier**: Match tier to use case to optimize cost/quality

### Debug Mode

```bash
# Enable verbose output
python scripts/generate_3d_model.py \
  --image input.jpg \
  --tier Gen-2.5-Medium \
  --output ./output \
  --api-key $HYPER3D_API_KEY 2>&1 | tee generation.log
```

## Performance Optimization

### Speed vs Quality Tradeoffs

| Scenario | Recommended Settings |
|----------|---------------------|
| Fast iteration | `Gen-2.5-Extreme-Low`, `quality=extra-low` |
| Preview renders | `Gen-2.5-Low`, `quality=low` |
| Production assets | `Gen-2.5-High`, `quality=high`, `hd_texture` |
| Archival quality | `Gen-2.5-Extreme-High`, `quality=high`, `HighPack` |

### Batch Processing Tips

- Process sequentially to avoid API rate limits
- Use consistent seeds for reproducibility
- Parallelize across multiple API keys if available

## API Key Management

### API Key Priority
The skill uses API keys in the following priority order:
1. **Command Line**: `--api-key` argument (highest priority)
2. **Environment Variable**: `HYPER3D_API_KEY`
3. **Free Test Key**: `vibecoding` (automatically used when no key is provided)

### Free Test Key
A free test API key (`vibecoding`) is built-in for evaluation purposes:
- **Usage**: Automatically used when no API key is specified
- **Limitations**: Has usage restrictions and rate limits
- **Recommendation**: Use for testing only; obtain a production key for regular use

### Production Key Setup
1. **Obtain Key**: Visit [Hyper3D API Dashboard](https://hyper3d.ai/api-dashboard)
2. **Set Environment Variable**:
   ```bash
   export HYPER3D_API_KEY="your_production_key_here"
   ```
3. **Persistent Storage** (recommended):
   ```bash
   echo 'HYPER3D_API_KEY=your_production_key_here' >> ~/.bashrc
   source ~/.bashrc
   ```

## Security Considerations

1. **API Key Protection**: Never commit keys to version control
2. **Environment Variables**: Use `HYPER3D_API_KEY` environment variable for production
3. **HTTPS Only**: All API communications use TLS 1.2+
4. **Input Sanitization**: Validate image paths before processing
5. **Free Key Limitations**: The built-in test key has usage limits; use production keys for critical workflows

## Version Compatibility

| Skill Version | API Version | Notes |
|---------------|-------------|-------|
| 2.0.0 | Gen-2.5 | Full Gen-2.5 feature support |
| 1.0.0 | Gen-2 | Legacy support maintained |

## Support & Resources

- **API Documentation**: [developer.hyper3d.ai/api-specification/rodin-gen2.5](https://developer.hyper3d.ai/api-specification/rodin-gen2.5)
- **Dashboard**: [hyper3d.ai/api-dashboard](https://hyper3d.ai/api-dashboard)
- **Support**: support@hyper3d.ai

## Changelog

### v2.1.0 (Fast Generation Mode)
- Added documentation for Fast Generation Mode with specific parameter combinations

### v2.0.0 (Gen-2.5 Upgrade)
- Added Gen-2.5 tier support (Extreme-Low, Low, Medium, High, Extreme-High)
- Added HD texture generation (`--hd-texture`)
- Added texture delight enhancement (`--texture-delight`)
- Added micro-object optimization (`--is-micro`)
- Added geometry instruction mode (`--geometry-instruct-mode`)
- Updated default tier to `Gen-2.5-Medium`
- Updated default mesh mode to `Raw`
- Enhanced error handling and logging

### v1.0.0
- Initial release with Gen-2 API support
- Image-to-3D and Text-to-3D generation
- Basic tier selection (Gen-2, Detail, Regular, Smooth, Sketch)