"""
Image preprocessing utilities.
"""
from io import BytesIO
from typing import Tuple
from PIL import Image
import numpy as np


def validate_image(image_bytes: bytes) -> Tuple[bool, str]:
    """
    Validate if uploaded file is a valid image.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        image = Image.open(BytesIO(image_bytes))
        image.verify()
        return True, "Valid image"
    except Exception as e:
        return False, f"Invalid image: {str(e)}"


def get_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """
    Load PIL Image from bytes.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        PIL Image object
    """
    return Image.open(BytesIO(image_bytes))


def get_image_info(image: Image.Image) -> dict:
    """
    Get image information.
    
    Args:
        image: PIL Image object
        
    Returns:
        Dictionary with image info
    """
    return {
        "size": image.size,
        "mode": image.mode,
        "format": image.format
    }
