#!/usr/bin/env python3
"""
Hyper3D Rodin Gen-2.5 Model Generator

This script generates 3D models from images or text prompts using the Hyper3D Rodin Gen-2.5 API.
"""

import os
import sys
import json
import argparse
from api_client import Hyper3DAPIClient
from image_utils import ImageUtils

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate 3D models from images or text prompts using Hyper3D Rodin Gen-2 API")
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--image", nargs='+', help="Path(s) to input image file(s) (up to 5 images)")
    mode_group.add_argument("--prompt", help="Text prompt to generate 3D model from")


    parser.add_argument("--tier", default="Gen-2.5-Medium",
                        choices=["Gen-2.5-Extreme-Low", "Gen-2.5-Low", "Gen-2.5-Medium", 
                                 "Gen-2.5-High", "Gen-2.5-Extreme-High",
                                 "Gen-2", "Smooth", "Regular", "Detail", "Sketch"],
                        help="API tier to use (Gen-2.5 tiers recommended for best quality)")
    
    parser.add_argument("--geometry-file-format", default="glb",
                        choices=["glb", "usdz", "fbx", "obj", "stl"],
                        help="Desired 3D model format")
    
    parser.add_argument("--quality", default="medium",
                        choices=["high", "medium", "low", "extra-low"],
                        help="Quality level for 3D model")
    
    parser.add_argument("--material", default="PBR",
                        choices=["PBR", "Shaded", "All"],
                        help="Material type")
    
    parser.add_argument("--mesh-mode", default="Quad",
                        choices=["Raw", "Quad"],
                        help="Mesh mode (Raw for triangular faces, Quad for quadrilateral faces)")
    
    parser.add_argument("--use-original-alpha", action="store_true",
                        help="Use original alpha channel from images")
    
    parser.add_argument("--seed", type=int, help="Seed value for randomization (0-65535)")
    
    parser.add_argument("--quality-override", type=int, 
                        help="Customize poly count (advanced parameter)")
    
    parser.add_argument("--tapose", action="store_true",
                        help="Generate T/A pose for human-like models")
    
    parser.add_argument("--bbox-condition", nargs=3, type=int, metavar=('WIDTH', 'HEIGHT', 'LENGTH'),
                        help="Bounding box condition [Width, Height, Length]")
    
    parser.add_argument("--addons", nargs='+', 
                        choices=["HighPack"],
                        help="Addons (e.g., HighPack for 4K textures)")
    
    parser.add_argument("--preview-render", action="store_true",
                        help="Generate additional preview render image")
    
    parser.add_argument("--hd-texture", action="store_true",
                        help="Generate HD texture (Gen-2.5 feature)")
    
    parser.add_argument("--texture-delight", action="store_true",
                        help="Use texture delight feature (Gen-2.5 feature)")
    
    parser.add_argument("--texture-mode", 
                        help="Texture mode (Gen-2.5 feature)")
    
    parser.add_argument("--is-micro", action="store_true",
                        help="Indicate the object is micro-sized (Gen-2.5 feature)")
    

    
    parser.add_argument("--geometry-instruct-mode", default="faithful",
                        help="Geometry instruction mode (Gen-2.5 feature, default: faithful)")
    
    parser.add_argument("--api-key", help="Hyper3D API key (overrides environment variable)")
    
    parser.add_argument("--output", help="Output directory for 3D model")
    
    parser.add_argument("--poll-interval", type=int, default=10,
                        help="Status check interval in seconds (default: 10)")
    
    parser.add_argument("--max-retries", type=int, default=60,
                        help="Maximum number of status check retries (default: 60)")
    
    args = parser.parse_args()
    
    try:
        # Check Hyper3D API key
        # Free test API key for evaluation purposes
        FREE_TEST_API_KEY = "vibecoding"
        env_api_key = os.environ.get("HYPER3D_API_KEY")
        
        # Priority: command line argument > environment variable > free test key
        if args.api_key:
            print("Using API key from command line argument")
            client = Hyper3DAPIClient(api_key=args.api_key)
        elif env_api_key:
            print(f"Using API key from environment variable: {env_api_key[:5]}...{env_api_key[-5:]}")
            client = Hyper3DAPIClient()
        else:
            # Use free test API key when no key is provided
            print(f"No API key provided. Using free test API key: {FREE_TEST_API_KEY}")
            print("Note: The free test key has usage limits. For production use, obtain your own API key from https://hyper3d.ai/api-dashboard")
            client = Hyper3DAPIClient(api_key=FREE_TEST_API_KEY)
            
        # Validate image input
        if args.image:
            print("Validating images...")
            for image_path in args.image:
                ImageUtils.validate_image(image_path)
            print("Image validation successful")
            
            input_images = []
            for image_path in args.image:
                input_images.append(image_path)
        else:
            input_images = None

        # Prepare parameters
        kwargs = {
            "images": input_images,
            "prompt": args.prompt,
            "tier": args.tier,
            "geometry_file_format": args.geometry_file_format,
            "quality": args.quality,
            "material": args.material,
            "mesh_mode": args.mesh_mode,
            "use_original_alpha": args.use_original_alpha,
            "seed": args.seed,
            "quality_override": args.quality_override,
            "TAPose": args.tapose,
            "bbox_condition": args.bbox_condition,
            "addons": args.addons,
            "preview_render": args.preview_render,
            "hd_texture": args.hd_texture,
            "texture_delight": args.texture_delight,
            "texture_mode": args.texture_mode,
            "is_micro": args.is_micro,
            "geometry_instruct_mode": args.geometry_instruct_mode
        }
        
        # Call API
        print(f"Calling Hyper3D Rodin Gen-2.5 API ...")
        print(f"Input parameters: {kwargs}")
        print("This may take a few minutes...")
        
        task_uuid, result = client.generate_3d_model(
            poll_interval=args.poll_interval,
            max_retries=args.max_retries,
            **kwargs
        )
        
        # Process result
        if "error" in result:
            print("\nAPI call failed:")
            print(json.dumps(result, indent=2))
        else:
            print("\n3D model generation successful!")
            
            # Extract download links
            file_list = result.get("list", [])
            
            if file_list:
                print(f"\nGenerated files ({len(file_list)}):")
                for i, file_info in enumerate(file_list, 1):
                    print(f"{i}. {file_info.get('name', 'Unknown')}")
                
                # If output directory is specified, download model
                if args.output:
                    # Create task-specific output directory
                    task_output_dir = os.path.join(args.output, task_uuid)
                    print(f"\nDownloading models to: {task_output_dir}")
                    for file_info in file_list:
                        download_model(file_info.get('url'), task_output_dir, file_info.get('name'))
            else:
                print("\nNo files found in download list")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

def download_model(model_url, output_dir, filename=None):
    """
    Download 3D model to specified directory
    
    Args:
        model_url: Model download link
        output_dir: Output directory
        filename: Filename (optional)
    """
    import requests
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get filename
    if not filename:
        filename = os.path.basename(model_url.split("?")[0])
    output_path = os.path.join(output_dir, filename)
    
    # Download file
    try:
        response = requests.get(model_url, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Downloaded: {output_path}")
        
    except Exception as e:
        print(f"Failed to download {filename}: {str(e)}")

if __name__ == "__main__":
    main()
