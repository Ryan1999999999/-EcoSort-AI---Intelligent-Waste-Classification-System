# EcoSort AI - Complete Development & Deployment Guide

## 📚 Documentation

This project is fully documented. Please read these guides in order:

1. **[BACKEND.md](./BACKEND.md)** - FastAPI backend setup & API documentation
2. **[FRONTEND.md](./FRONTEND.md)** - Vue.js 3 frontend setup & development
3. **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Docker deployment & production setup
4. **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Project overview & model details

## 🚀 Quick Start (5 Minutes)

### Option 1: Docker (Recommended for Production)

```bash
# 1. Build all services
docker-compose -f docker/docker-compose.yml build

# 2. Start services
docker-compose -f docker/docker-compose.yml up -d

# 3. Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Access at http://localhost:5173
```

## 📁 Project Structure

```
EcoSort-AI/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py            # API routes & startup
│   │   ├── core/
│   │   │   ├── inference.py   # ONNX model inference
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── schemas.py     # Pydantic models
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── preprocessing.py
│   │       └── __init__.py
│   ├── requirements.txt         # Python dependencies
│   └── .env.example
│
├── frontend/                   # Vue.js 3 + Vite
│   ├── src/
│   │   ├── views/             # Page components
│   │   │   ├── Home.vue
│   │   │   ├── Classify.vue
│   │   │   ├── Metrics.vue
│   │   │   └── Impact.vue
│   │   ├── components/
│   │   ├── api/
│   │   │   └── client.ts      # Axios API client
│   │   ├── stores/
│   │   │   └── predictionStore.ts # Pinia state management
│   │   ├── router/
│   │   │   └── index.ts
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── .env.example
│
├── docker/
│   ├── docker-compose.yml      # Multi-service orchestration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── nginx.conf
│   └── default.conf
│
├── models/
│   └── best_model.onnx         # Trained ONNX model (314MB)
│
├── notebooks/
│   └── 01_trashnet_training.ipynb
│
├── docs/
│   ├── BACKEND.md              # Backend documentation
│   ├── FRONTEND.md             # Frontend documentation
│   ├── DEPLOYMENT.md            # Docker & production setup
│   ├── PROJECT_SUMMARY.md      # Project overview
│   └── DEVELOPMENT.md          # This file
│
├── README.md
└── requirements.txt
```

## 🎯 What Each Component Does

### Backend (FastAPI)
- **Port:** 8000
- **Purpose:** REST API for waste classification
- **Key Features:**
  - ONNX model inference
  - Image preprocessing (resize, normalize)
  - Pydantic request/response validation
  - CORS support
  - Health checks

### Frontend (Vue.js 3)
- **Port:** 5173 (dev) / 80 (prod)
- **Purpose:** Web interface for image classification
- **Key Features:**
  - Drag-and-drop image upload
  - Real-time predictions
  - Classification history
  - Performance metrics
  - Environmental impact tracking

### Docker Setup
- **Services:**
  - Backend (FastAPI) - Port 8000
  - Frontend (Nginx) - Port 80/3000
  - MLflow (Optional) - Port 5000

## 🔌 API Endpoints

### Core Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/model/info` | Model information |
| GET | `/classes` | Available waste classes |
| POST | `/predict` | Classify waste image |

### Request/Response Examples

**Predict:**
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@waste_image.jpg"
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
  "impact_message": "Most plastics take 400+ years to decompose..."
}
```

## 🛠️ Common Tasks

### Running Backend Tests
```bash
cd backend
python -m pytest
```

### Building Frontend for Production
```bash
cd frontend
npm run build
```

### Viewing Docker Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Follow in real-time
docker-compose logs -f frontend
```

### Stopping Services
```bash
# Stop all
docker-compose down

# Stop with volume cleanup
docker-compose down -v
```

## 🔑 Key Technologies

- **Framework:** FastAPI + Vue.js 3
- **ML Inference:** ONNX Runtime
- **Model:** MobileNetV3 Large
- **State Management:** Pinia
- **HTTP Client:** Axios
- **UI Components:** Element Plus
- **Containerization:** Docker & Docker Compose
- **Web Server:** Nginx

## 📊 Model Details

- **Name:** MobileNetV3 Large
- **Task:** 6-class waste classification
- **Accuracy:** 92.88% on validation set
- **Classes:** Cardboard, Glass, Metal, Paper, Plastic, Trash
- **Input Size:** 320x320
- **Format:** ONNX (optimized for inference)
- **Size:** ~314 MB
- **Inference Time:** ~50-100ms per image (CPU)

## 🚀 Deployment Steps

### Local Development
1. Clone/navigate to project
2. Set up backend virtual environment
3. Install Python dependencies
4. Set up frontend Node.js environment
5. Install npm packages
6. Start backend server
7. Start frontend dev server
8. Access http://localhost:5173

### Docker Deployment
1. Ensure model file exists
2. Build Docker images
3. Run docker-compose
4. Access http://localhost:3000

### Production Deployment
1. Configure environment variables
2. Set up SSL/HTTPS
3. Configure domain/DNS
4. Deploy to cloud infrastructure (AWS, GCP, Azure, etc.)
5. Set up monitoring & logging
6. Configure backups

## ✅ Verification Checklist

**Backend:**
- [ ] Backend starts without errors
- [ ] Health check passes (http://localhost:8000/health)
- [ ] Can see API docs (http://localhost:8000/docs)
- [ ] Model loads successfully

**Frontend:**
- [ ] Frontend dev server starts
- [ ] Page loads at http://localhost:5173
- [ ] No CORS errors in console
- [ ] Can navigate between pages

**Integration:**
- [ ] Frontend can connect to backend
- [ ] Can upload image successfully
- [ ] Predictions return correct format
- [ ] Classification history populates
- [ ] Metrics page updates

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Check error logs
python -m uvicorn app.main:app --reload
```

### Frontend Can't Connect to Backend
```bash
# Check CORS configuration
# Update frontend .env if needed
echo "VITE_API_URL=http://localhost:8000" > .env
```

### Docker Build Fails
```bash
# Clear cache and rebuild
docker system prune
docker-compose build --no-cache
```

### Out of Memory
```bash
# Reduce model preprocessing batch size
# Or increase system memory
```

## 📈 Performance Tips

1. **Use GPU:** Configure ONNX Runtime for CUDA
2. **Cache Model:** Load model once at startup
3. **Compress Images:** Frontend compresses before upload
4. **Use CDN:** Serve frontend static files from CDN
5. **Monitor Resources:** Use docker stats regularly

## 🔐 Security Considerations

- [ ] HTTPS/SSL enabled in production
- [ ] CORS restricted to allowed domains
- [ ] Input validation on all endpoints
- [ ] File size limits enforced
- [ ] Environment variables not committed
- [ ] Database credentials secured
- [ ] Regular security updates

## 📞 Support

For detailed documentation, see:
- **Backend Issues:** [BACKEND.md](./BACKEND.md#troubleshooting)
- **Frontend Issues:** [FRONTEND.md](./FRONTEND.md#troubleshooting)
- **Deployment Issues:** [DEPLOYMENT.md](./DEPLOYMENT.md#troubleshooting)

## 🎉 You're All Set!

The project is now fully configured and ready to use. Start by reading the backend and frontend guides for detailed information on each component.

---

**Last Updated:** April 2024  
**Project Version:** 1.0.0  
**Status:** Production Ready
