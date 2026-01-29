import base64
import os
from PIL import Image

class ImageUtils:
    """Images tools"""

    SUPPORTED_FORMATS = {
        "JPEG": [".jpg", ".jpeg"],
        "PNG": [".png"],
        "WEBP": [".webp"],
    }
    
    # Image size limits
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    MIN_RESOLUTION = (512, 512)
    MAX_RESOLUTION = (4096, 4096)
    
    @classmethod
    def validate_image(cls, image_path):
        """
        image validate
        
        Args:
            image_path: Image file path
            
        Returns:
            bool: Image is valid
            
        Raises:
            Exception: If image is invalid
        """
        # Check if file exists
        if not os.path.exists(image_path):
            raise Exception("Image file does not exist")
        
        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > cls.MAX_FILE_SIZE:
            raise Exception(f"Image file size exceeds {cls.MAX_FILE_SIZE // (1024 * 1024)}MB limit")
        
        # Check file extension
        ext = os.path.splitext(image_path)[1].lower()
        valid_extensions = []
        for formats in cls.SUPPORTED_FORMATS.values():
            valid_extensions.extend(formats)
        
        if ext not in valid_extensions:
            raise Exception(f"Unsupported image format. Please use one of: {', '.join(valid_extensions)}")
        
        # Check image resolution
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                if width < cls.MIN_RESOLUTION[0] or height < cls.MIN_RESOLUTION[1]:
                    raise Exception(f"Image resolution is too low. Minimum resolution is {cls.MIN_RESOLUTION[0]}x{cls.MIN_RESOLUTION[1]}")
                
                if width > cls.MAX_RESOLUTION[0] or height > cls.MAX_RESOLUTION[1]:
                    raise Exception(f"Image resolution is too high. Maximum resolution is {cls.MAX_RESOLUTION[0]}x{cls.MAX_RESOLUTION[1]}")
        
        except Exception as e:
            raise Exception(f"Failed to validate image: {str(e)}")
        
        return True
