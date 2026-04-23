from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

from .core.inference import WasteClassifier
from app.models.schemas import PredictionResponse, ModelInfo, HealthResponse, ClassesResponse
from app.utils.preprocessing import validate_image, get_image_from_bytes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EcoSort AI API",
    description="Intelligent Waste Classification System",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production (e.g., ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global classifier instance
classifier = None


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup."""
    global classifier
    try:
        classifier = WasteClassifier()
        if classifier.is_model_loaded():
            logger.info("✓ WasteClassifier initialized successfully")
        else:
            logger.warning("⚠️  WasteClassifier initialized but model not loaded. API will start without predictions.")
    except Exception as e:
        logger.error(f"✗ Failed to initialize WasteClassifier: {str(e)}")
        # Don't raise - allow API to start without model


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down EcoSort AI API")


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health Check Endpoint"
)
async def health():
    """
    Check if the API is running and model is loaded.
    
    Returns:
        HealthResponse with system status
    """
    if classifier is None:
        return HealthResponse(
            status="degraded",
            model_loaded=False,
            model_name="MobileNetV3 Large"
        )
    
    return HealthResponse(
        status="healthy" if classifier.is_model_loaded() else "degraded",
        model_loaded=classifier.is_model_loaded(),
        model_name="MobileNetV3 Large"
    )


@app.get(
    "/model/info",
    response_model=ModelInfo,
    tags=["Model Information"],
    summary="Get Model Information"
)
async def model_info():
    """
    Get detailed information about the loaded model.
    
    Returns:
        ModelInfo with model details
    """
    if classifier is None or not classifier.is_model_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Regenerate the ONNX model from the training notebook."
        )
    
    return classifier.get_model_info()


@app.get(
    "/classes",
    response_model=ClassesResponse,
    tags=["Model Information"],
    summary="Get Available Waste Classes"
)
async def get_classes():
    """
    Get all available waste classification classes.
    
    Returns:
        ClassesResponse with class mappings
    """
    if classifier is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Classifier not initialized"
        )
    
    return ClassesResponse(classes=classifier.get_classes())


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Inference"],
    summary="Classify Waste Material",
    responses={
        200: {"description": "Successful prediction"},
        400: {"description": "Invalid image format"},
        422: {"description": "Unprocessable entity"},
        503: {"description": "Service unavailable"}
    }
)
async def predict(file: UploadFile = File(..., description="Image file to classify (JPEG, PNG)")):
    """
    Classify a waste material from an uploaded image.
    
    ### Request
    - **file**: Image file (JPEG, PNG)
    
    ### Response
    - **predicted_class**: The waste material class (cardboard, glass, metal, paper, plastic, trash)
    - **confidence**: Classification confidence (0-100%)
    - **all_scores**: Confidence scores for each class
    - **impact_message**: Environmental impact information
    
    ### Example Usage
    ```bash
    curl -X POST "http://localhost:8000/predict" \\
      -H "Content-Type: multipart/form-data" \\
      -F "file=@image.jpg"
    ```
    """
    if classifier is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not initialized. Please check server logs."
        )
    
    if not classifier.is_model_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model failed to load. This is likely due to a corrupted ONNX file. Please regenerate the model from the training notebook."
        )
    
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type: {file.content_type}. Expected image file."
            )
        
        # Read and validate image
        image_bytes = await file.read()
        is_valid, validation_msg = validate_image(image_bytes)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation_msg
            )
        
        # Load image and make prediction
        image = get_image_from_bytes(image_bytes)
        prediction = classifier.predict(image)
        
        logger.info(f"✓ Prediction: {prediction['predicted_class']} (confidence: {prediction['confidence']}%)")
        
        return PredictionResponse(
            predicted_class=prediction['predicted_class'],
            confidence=prediction['confidence'],
            all_scores=prediction['all_scores'],
            impact_message=prediction['impact_message']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during prediction: {str(e)}"
        )


@app.get("/", tags=["Documentation"])
async def root():
    """
    Welcome endpoint. Access API documentation at /docs
    """
    return {
        "message": "Welcome to EcoSort AI",
        "docs": "http://localhost:8000/docs",
        "endpoints": {
            "health": "GET /health",
            "model_info": "GET /model/info",
            "classes": "GET /classes",
            "predict": "POST /predict"
        }
    }


# Exception handlers for better error responses
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )