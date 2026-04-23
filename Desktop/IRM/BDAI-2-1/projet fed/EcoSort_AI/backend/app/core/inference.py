"""
ONNX Model inference engine for waste classification.
"""
import os
from pathlib import Path
from typing import Dict, Tuple, Any, List
import numpy as np
import onnxruntime as ort
from PIL import Image

from app.models.schemas import ModelInfo


class WasteClassifier:
    """
    Handles ONNX model loading and inference for waste classification.
    """
    
    # Class mapping
    CLASS_MAPPING = {
        0: "cardboard",
        1: "glass",
        2: "metal",
        3: "paper",
        4: "plastic",
        5: "trash"
    }
    
    # Environmental impact messages for each class
    IMPACT_MESSAGES = {
        "cardboard": "Cardboard is highly recyclable! This material can be processed 5-7 times before degrading. Recycling tons of cardboard annually saves 24 trees and 4,000 gallons of water.",
        "glass": "Glass is 100% recyclable and can be reused indefinitely! One recycled glass bottle saves enough energy to power a laptop for 3 hours.",
        "metal": "Metal is infinitely recyclable! Recycling aluminum uses 95% less energy than mining new metal. A single aluminum can saves enough electricity to power a laptop for 3 hours.",
        "paper": "Paper is recyclable, but not endlessly. After 7 recycling cycles, paper fibers become too short to use. Reducing paper consumption is even better than recycling.",
        "plastic": "Most plastics take 400+ years to decompose. Only ~9% of plastic ever produced has been recycled. Choose reusable alternatives when possible!",
        "trash": "This item appears to be general waste. Consider if any components can be separated for recycling or proper disposal."
    }
    
    def __init__(self, model_path: str = None):
        """
        Initialize the waste classifier with ONNX model.
        
        Args:
            model_path: Path to the ONNX model file. If None, uses default location.
        """
        if model_path is None:
            # Default model path relative to project root
            project_root = Path(__file__).parent.parent.parent.parent
            model_path = project_root / "models" / "best_model.onnx"
        
        self.model_path = Path(model_path)
        self.session = None
        self.input_name = None
        self.output_name = None
        self.is_loaded = False
        
        self._load_model()
    
    def _load_model(self):
        """Load ONNX model and initialize inference session."""
        if not self.model_path.exists():
            print(f"⚠️  WARNING: Model file not found at {self.model_path}")
            print(f"   The API will start, but predictions will not work.")
            self.is_loaded = False
            return
        
        # Verify model file is not empty
        file_size = self.model_path.stat().st_size
        if file_size < 100 * 1024 * 1024:  # Less than 100MB likely corrupted
            print(f"⚠️  WARNING: Model file is only {file_size / 1024 / 1024:.1f}MB (expected ~314MB)")
            print("⚠️  Model may be corrupted. Please re-export from training notebook.")
        
        try:
            # Create ONNX Runtime session with optimized settings
            session_options = ort.SessionOptions()
            session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
            
            # Use CPU provider (can add CUDA if available)
            providers = ['CPUExecutionProvider']
            
            print(f"📂 Loading model from: {self.model_path}")
            print(f"📊 File size: {file_size / 1024 / 1024:.1f}MB")
            print(f"⏳ Initializing ONNX Runtime session...")
            
            self.session = ort.InferenceSession(
                str(self.model_path),
                sess_options=session_options,
                providers=providers
            )
            
            # Get input and output names
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            
            self.is_loaded = True
            print(f"✓ Model loaded successfully!")
            print(f"  - Input name: {self.input_name}")
            print(f"  - Output name: {self.output_name}")
        except Exception as e:
            print(f"⚠️  WARNING: Failed to load ONNX model")
            print(f"   Error type: {type(e).__name__}")
            print(f"   Error message: {str(e)}")
            print(f"   Model path: {self.model_path}")
            print(f"   File size: {file_size / 1024 / 1024:.1f}MB")
            print(f"   → The API will start, but predictions will not work.")
            print(f"   → Please regenerate the model from the training notebook.")
            self.is_loaded = False
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.is_loaded
    
    def get_model_info(self) -> ModelInfo:
        """Get model information."""
        return ModelInfo(
            name="MobileNetV3 Large",
            version="1.0.0",
            accuracy=92.88,
            num_classes=6,
            input_shape=[1, 3, 320, 320],
            framework="ONNX",
            description="Optimized waste classification model trained on TrashNet dataset"
        )
    
    def get_classes(self) -> Dict[int, str]:
        """Get available waste classes."""
        return self.CLASS_MAPPING
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for model inference.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image as numpy array (1, 3, 320, 320)
        """
        # Resize to target size (320x320)
        target_size = (320, 320)
        image = image.convert('RGB')  # Ensure RGB format
        image_resized = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize to [0, 1]
        image_array = np.array(image_resized, dtype=np.float32) / 255.0
        
        # Normalize using ImageNet statistics
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        
        # Apply normalization: (x - mean) / std
        image_array = (image_array - mean) / std
        
        # Convert to CHW format (Channel, Height, Width)
        image_array = np.transpose(image_array, (2, 0, 1))
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array.astype(np.float32)
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """
        Predict waste class for an image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary containing:
                - predicted_class: The predicted waste class
                - confidence: Confidence percentage (0-100)
                - all_scores: Confidence for each class
                - impact_message: Environmental message for the class
        """
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")
        
        # Preprocess image
        image_array = self.preprocess_image(image)
        
        # Run inference
        outputs = self.session.run([self.output_name], {self.input_name: image_array})
        logits = outputs[0]
        
        # Get probabilities using softmax
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        probabilities = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        
        # Get prediction
        predicted_class_idx = int(np.argmax(probabilities[0]))
        predicted_class = self.CLASS_MAPPING[predicted_class_idx]
        confidence = float(probabilities[0][predicted_class_idx]) * 100
        
        # Get confidence scores for all classes
        all_scores = {
            self.CLASS_MAPPING[i]: float(probabilities[0][i]) * 100 
            for i in range(len(self.CLASS_MAPPING))
        }
        
        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 2),
            "all_scores": {k: round(v, 2) for k, v in all_scores.items()},
            "impact_message": self.IMPACT_MESSAGES[predicted_class]
        }
