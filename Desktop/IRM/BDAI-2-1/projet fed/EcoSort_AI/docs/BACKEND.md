# EcoSort AI - Backend Setup Guide

## 📋 Overview

The FastAPI backend provides REST API endpoints for waste classification using the trained ONNX model. It includes:
- Image upload and inference
- Real-time predictions with confidence scores
- Environmental impact messages
- Health checks and model information endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- ONNX Runtime
- FastAPI + Uvicorn

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit .env if needed (defaults should work for local development)
cat .env
```

### Step 3: Verify Model File

Ensure `models/best_model.onnx` exists:
```bash
ls -lh ../models/best_model.onnx
```

### Step 4: Run Development Server

```bash
cd ..
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
✓ WasteClassifier initialized successfully
```

## 📚 API Documentation

Access interactive API docs at: **http://localhost:8000/docs**

### Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "MobileNetV3 Large"
}
```

#### 2. Model Information
```bash
curl http://localhost:8000/model/info
```

**Response:**
```json
{
  "name": "MobileNetV3 Large",
  "version": "1.0.0",
  "accuracy": 92.88,
  "num_classes": 6,
  "input_shape": [1, 3, 320, 320],
  "framework": "ONNX",
  "description": "Optimized waste classification model trained on TrashNet dataset"
}
```

#### 3. Available Classes
```bash
curl http://localhost:8000/classes
```

**Response:**
```json
{
  "classes": {
    "0": "cardboard",
    "1": "glass",
    "2": "metal",
    "3": "paper",
    "4": "plastic",
    "5": "trash"
  }
}
```

#### 4. Predict (Main Endpoint) ⭐
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

**Response:**
```json
{
  "predicted_class": "plastic",
  "confidence": 94.23,
  "all_scores": {
    "cardboard": 2.5,
    "glass": 1.2,
    "metal": 0.8,
    "paper": 1.3,
    "plastic": 94.23,
    "trash": 0.01
  },
  "impact_message": "Most plastics take 400+ years to decompose. Only ~9% of plastic ever produced has been recycled. Choose reusable alternatives when possible!"
}
```

## 🧪 Testing the API

### Using Python
```python
import requests
from pathlib import Path

# Upload image and get prediction
image_path = Path("path/to/waste_image.jpg")
files = {"file": open(image_path, "rb")}
response = requests.post("http://localhost:8000/predict", files=files)
print(response.json())
```

### Using cURL
```bash
# Health check
curl -s http://localhost:8000/health | jq

# Predict
curl -X POST http://localhost:8000/predict \
  -F "file=@waste_image.jpg" | jq
```

### Using Postman
1. Create new POST request
2. URL: `http://localhost:8000/predict`
3. Body → form-data
4. Key: `file` (type: File)
5. Value: Select image file
6. Send

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app & routes
│   ├── core/
│   │   ├── __init__.py
│   │   └── inference.py        # ONNX model inference
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic request/response models
│   └── utils/
│       ├── __init__.py
│       └── preprocessing.py    # Image preprocessing
├── requirements.txt             # Dependencies
├── .env.example                # Environment template
└── README.md
```

## ⚙️ Configuration

### Environment Variables

Edit `.env` to customize:

```env
# API Server
HOST=0.0.0.0
PORT=8000
ENV=development
LOG_LEVEL=info

# CORS - Update with your frontend URL
CORS_ORIGINS=["http://localhost:5173"]

# Model
MODEL_PATH=./models/best_model.onnx
MAX_FILE_SIZE=10485760  # 10MB
```

### CORS Configuration

For production, update `app/main.py` CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
cd ..
docker build -f docker/Dockerfile.backend -t ecosort-backend:latest .
```

### Run Container
```bash
docker run -p 8000:8000 ecosort-backend:latest
```

Access at: `http://localhost:8000/docs`

### With Docker Compose
```bash
docker-compose -f docker/docker-compose.yml up backend
```

## 🔍 Troubleshooting

### Issue: Model not found
```
FileNotFoundError: Model not found at ./models/best_model.onnx
```

**Solution:**
```bash
# Check if model exists
ls -lh models/best_model.onnx

# If missing, verify it's in the models directory
# Ensure you're running from project root
```

### Issue: Port 8000 already in use
```bash
# Use different port
uvicorn app.main:app --port 8001 --reload
```

### Issue: CORS errors from frontend
Update `CORS_ORIGINS` in `.env` or `app/main.py`:
```python
allow_origins=[
    "http://localhost:5173",      # Vite dev server
    "http://localhost:3000",      # Alternative
    "https://yourdomain.com"      # Production
]
```

### Issue: Out of memory during inference
Reduce batch size or use lighter model format.

## 📊 Performance

- **Model Size:** ~27 MB (ONNX)
- **Inference Time:** ~50-100ms per image
- **Memory Usage:** ~200-300 MB
- **Throughput:** ~10 predictions/second CPU, ~50+ GPU

## 🔐 Security Notes

1. **Input Validation:** All inputs validated through Pydantic
2. **File Size Limit:** 10MB max (configurable)
3. **File Type Check:** Only images accepted
4. **Error Messages:** Generic in production to avoid info leakage

For production:
- Use HTTPS only
- Implement authentication (JWT, API keys)
- Rate limiting
- Request logging

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| onnxruntime | 1.16.3 | Model inference |
| numpy | 1.24.3 | Numerical computing |
| pillow | 10.0.0 | Image processing |
| pydantic | 2.5.0 | Data validation |

## 🚀 Next Steps

1. **Frontend:** Build Vue.js 3 interface
2. **Integration:** Connect frontend to backend
3. **Testing:** Run end-to-end tests
4. **Deployment:** Deploy with Docker Compose

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ONNX Runtime](https://onnxruntime.ai/)
- [Pydantic v2](https://docs.pydantic.dev/)
