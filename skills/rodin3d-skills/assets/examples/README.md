# Example Assets

This directory contains example assets for the rodin3d-skills project.

## Purpose

The examples provided here are intended to:

1. Demonstrate how to use the Hyper3D Rodin Gen-2 API
2. Show best practices for image preparation
3. Provide sample prompts for text-to-3D generation
4. Serve as a reference for expected output formats

## Usage

To use these examples, run the generate_3d_model.py script with the appropriate parameters:

### From Image

```bash
python scripts/generate_3d_model.py --image path/to/example/image.jpg
```

### From Text Prompt

```bash
python scripts/generate_3d_model.py --prompt "A detailed 3D model of a futuristic spaceship"
```

## Example Prompts

Here are some example prompts for text-to-3D generation:

1. "A detailed 3D model of a medieval castle"
2. "A futuristic cityscape with flying cars"
3. "A realistic 3D model of a cat sitting on a couch"
4. "An abstract sculpture made of glass and metal"
5. "A 3D model of a cozy cottage in the woods"

## Best Practices

### For Image Inputs

1. Use high-resolution images (at least 1024x1024 pixels)
2. Ensure good lighting and clear details
3. Avoid cluttered backgrounds
4. Use multiple angles for better results
5. Optimize images before submission

### For Text Prompts

1. Be specific and detailed
2. Mention materials and textures
3. Include lighting information
4. Specify the style (realistic, cartoon, futuristic, etc.)
5. Provide context for the object

## Output Formats

The API supports the following output formats:

- GLB (recommended for web and most 3D software)
- USDZ (for Apple platforms)
- FBX (for game engines and 3D modeling software)
- OBJ (universal 3D format)
- STL (for 3D printing)

Choose the format that best suits your needs.
