import os
import requests
import time

class Hyper3DAPIClient:
    """Hyper3D Rodin Gen-2 API client for handling API communication"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("HYPER3D_API_KEY")
        self.api_url = "https://api.hyper3d.com/api/v2/rodin"
        self.status_url = "https://api.hyper3d.com/api/v2/status"
        self.download_url = "https://api.hyper3d.com/api/v2/download"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def submit_generation_task(self, images=None, prompt=None, tier="Gen-2", geometry_file_format="glb", 
                          material="PBR", quality="medium", use_original_alpha=False,
                          seed=None, quality_override=None, TAPose=False,
                          bbox_condition=None, mesh_mode="Quad", addons=None,
                          preview_render=False):
        """
        Submit 3D model generation task to Hyper3D Rodin Gen-2 API
        
        Args:
            images: List of image files (up to 5 images)
            prompt: Text prompt (optional)
            tier: Generation tier (default "Gen-2", options: "Smooth", "Regular", "Detail", "Sketch")
            geometry_file_format: Output format ("glb", "usdz", "fbx", "obj", "stl")
            material: Material type ("PBR", "Shaded", "All")
            quality: Quality level ("high", "medium", "low", "extra-low")
            use_original_alpha: Whether to use original alpha channel (default False)
            seed: Random seed value (0-65535)
            quality_override: Custom polygon count
            TAPose: Whether to generate T/A pose (default False)
            bbox_condition: Bounding box condition array [Width, Height, Length]
            mesh_mode: Mesh mode ("Raw" or "Quad")
            addons: Addon features list (e.g., ["HighPack"])
            preview_render: Whether to generate preview render (default False)
            
        Returns:
            dict: API response data containing subscription_key
        """
        if not self.api_key:
            raise ValueError("API key is required. Please set HYPER3D_API_KEY environment variable or pass it to the constructor.")
        
        # Prepare multipart/form-data
        files = []
        if images:
            for image in images:
                # Check if image is file path or file object
                if isinstance(image, str):
                    # If it's a file path, open the file and read its content
                    with open(image, 'rb') as f:
                        files.append(('images', (os.path.basename(image), f.read())))
                else:
                    # If it's a file object, use it directly
                    files.append(('images', image))
        
        data = {
            "tier": tier,
            "geometry_file_format": geometry_file_format,
            "material": material,
            "quality": quality,
            "use_original_alpha": str(use_original_alpha).lower(),
            "TAPose": str(TAPose).lower(),
            "preview_render": str(preview_render).lower()
        }
        
        # Add optional parameters
        if prompt:
            data["prompt"] = prompt
        
        if seed is not None:
            data["seed"] = str(seed)
        
        if quality_override is not None:
            data["quality_override"] = str(quality_override)
        
        if bbox_condition:
            data["bbox_condition"] = ",".join(map(str, bbox_condition))
        
        if mesh_mode:
            data["mesh_mode"] = mesh_mode
        
        if addons:
            data["addons"] = ",".join(addons)
        
        try:
            # Send API request (using multipart/form-data)
            response = requests.post(
                self.api_url,
                headers=self.headers,
                files=files,
                data=data,
                timeout=300  # 5 minutes timeout
            )
            
            # Check response status
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def check_task_status(self, subscription_key):
        """
        Check task status
        
        Args:
            subscription_key: Task subscription key
            
        Returns:
            dict: Task status information
        """
        try:
            response = requests.post(
                self.status_url,
                headers=self.headers,
                json={"subscription_key": subscription_key},
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Status check failed: {str(e)}")
    
    def download_results(self, task_uuid):
        """
        Get download links
        
        Args:
            task_uuid: Task UUID
            
        Returns:
            dict: Download links list
        """
        try:
            response = requests.post(
                self.download_url,
                headers=self.headers,
                json={"task_uuid": task_uuid},
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Download request failed: {str(e)}")
    
    def generate_3d_model(self, images=None, prompt=None, tier="Gen-2", geometry_file_format="glb", 
                        quality="medium", material="PBR", mesh_mode="Quad",
                        use_original_alpha=False, seed=None, quality_override=None,
                        TAPose=False, bbox_condition=None, addons=None,
                        preview_render=False, poll_interval=10, max_retries=60):
        """
        Complete 3D model generation process: submit task, poll status, get download links
        
        Args:
            images: List of image files (up to 5 images)
            prompt: Text prompt (optional)
            tier: Generation tier (default "Gen-2", options: "Smooth", "Regular", "Detail", "Sketch")
            geometry_file_format: Output format ("glb", "usdz", "fbx", "obj", "stl")
            quality: Quality level ("high", "medium", "low", "extra-low")
            material: Material type ("PBR", "Shaded", "All")
            mesh_mode: Mesh mode ("Raw" or "Quad")
            use_original_alpha: Whether to use original alpha channel (default False)
            seed: Random seed value (0-65535)
            quality_override: Custom polygon count
            TAPose: Whether to generate T/A pose (default False)
            bbox_condition: Bounding box condition array [Width, Height, Length]
            addons: Addon features list (e.g., ["HighPack"])
            preview_render: Whether to generate preview render (default False)
            poll_interval: Polling interval in seconds
            max_retries: Maximum number of retries
            
        Returns:
            tuple: (task_uuid, dict) containing task uuid and model download links
        """
        # Submit generation task
        print("Submitting generation task...")
        submit_result = self.submit_generation_task(
            images=images,
            prompt=prompt,
            tier=tier,
            geometry_file_format=geometry_file_format,
            quality=quality,
            material=material,
            mesh_mode=mesh_mode,
            use_original_alpha=use_original_alpha,
            seed=seed,
            quality_override=quality_override,
            TAPose=TAPose,
            bbox_condition=bbox_condition,
            addons=addons,
            preview_render=preview_render
        )
        
        if "error" in submit_result:
            raise Exception(f"Task submission failed: {submit_result.get('error')}")
        
        task_uuid = submit_result.get("uuid")

        subscription_key = submit_result.get("jobs").get("subscription_key")
        
        # Poll task status
        for attempt in range(max_retries):
            print(f"Checking task status... (Attempt {attempt + 1}/{max_retries})")
            
            status_result = self.check_task_status(subscription_key)
            
            if "error" in status_result:
                raise Exception(f"Status check failed: {status_result.get('error')}")
            
            jobs = status_result.get("jobs", [])
            if not jobs:
                raise Exception("No jobs found in status response")

            status = []
            done_count = 0
            total_count = len(jobs)

            for job in jobs:
                status.append(job.get("status"))
                if job.get("status") == "Done":
                    done_count += 1
            
            print(f"Current status: ({done_count}/{total_count} done)")
            
            if all(s == "Done" for s in status):
                print("Task completed successfully!")
                download_result = self.download_results(task_uuid)
                return task_uuid, download_result
            elif any(s == "Failed" for s in status):
                raise Exception(f"Task failed: {job.get('error', 'Unknown error')}")
            elif any(s == "Waiting" for s in status):
                print("Task is waiting in queue...")
            elif any(s == "Generating" for s in status):
                print("Task is being processed...")
            
            # Continue polling
            time.sleep(poll_interval)
        
        raise Exception("Task processing timed out")
