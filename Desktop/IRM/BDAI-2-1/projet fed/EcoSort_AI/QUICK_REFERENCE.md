# 🚀 EcoSort AI - Quick Reference Card

## Start Services Immediately

### Docker (Recommended)
```bash
docker-compose -f docker/docker-compose.yml up -d
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development
```bash
# Terminal 1: Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend  
cd frontend && npm install && npm run dev
# Access: http://localhost:5173
```

---

## Key URLs

| Service | URL | Port |
|---------|-----|------|
| Web App | http://localhost:3000 | Frontend |
| API Docs | http://localhost:8000/docs | Backend |
| Metrics | http://localhost:3000/metrics | UI |
| Impact | http://localhost:3000/impact | UI |

---

## API Endpoints

```bash
# Health Check
curl http://localhost:8000/health

# Classify Image
curl -X POST http://localhost:8000/predict \
  -F "file=@image.jpg"

# Get Classes
curl http://localhost:8000/classes

# Model Info
curl http://localhost:8000/model/info
```

---

## Project Features

✅ **ML Model**: MobileNetV3 Large (92.88% accuracy)  
✅ **6 Classes**: Cardboard, Glass, Metal, Paper, Plastic, Trash  
✅ **Real-time**: 50-100ms inference time  
✅ **Responsive**: Mobile-friendly design  
✅ **Deployed**: Ready for production  

---

## File Organization

```
EcoSort-AI/
├── backend/          ← FastAPI (port 8000)
├── frontend/         ← Vue.js (port 5173/3000)
├── docker/          ← Docker configs
├── models/          ← ONNX model (best_model.onnx)
├── docs/            ← Documentation (6 guides)
└── notebooks/       ← Training notebook
```

---

## Documentation

Start here → **GETTING_STARTED.md** (5 min)

Then read:
- DEVELOPMENT.md (Overview)
- BACKEND.md (API details)
- FRONTEND.md (UI details)
- DEPLOYMENT.md (Production)

---

## Model Info

- **Name**: MobileNetV3 Large
- **Task**: 6-class waste classification
- **Accuracy**: 92.88%
- **Format**: ONNX
- **Size**: 314MB
- **Speed**: ~75ms per image (average)

---

## Tech Stack

```
Backend  → FastAPI + ONNX Runtime
Frontend → Vue.js 3 + Vite + Element Plus
Deploy   → Docker + Docker Compose + Nginx
```

---

## Development Commands

### Backend
```bash
# Install deps
pip install -r requirements.txt

# Run server
python -m uvicorn app.main:app --reload

# Run tests
pytest
```

### Frontend
```bash
# Install deps
npm install

# Dev server
npm run dev

# Build for production
npm run build

# Preview build
npm run preview
```

### Docker
```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Use: `--port 8001` |
| Port 5173 in use | Vite will try next port |
| Can't connect APIs | Check CORS in backend/app/main.py |
| Docker fail | `docker system prune -a` |
| Model not found | Verify `models/best_model.onnx` exists |

---

## Environment Variables

### Backend (.env)
```
HOST=0.0.0.0
PORT=8000
ENV=production
MODEL_PATH=./models/best_model.onnx
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=EcoSort AI
```

---

## Performance

- **Inference**: 50-100ms (CPU)
- **Throughput**: 10+ predictions/sec
- **Memory**: 300-500MB
- **Model Size**: 314MB
- **Accuracy**: 92.88%

---

## Key Features Ready

✅ Image Upload (drag & drop)  
✅ Real-time Predictions  
✅ Confidence Scores  
✅ Classification History  
✅ Performance Metrics  
✅ Environmental Impact  
✅ Health Checks  
✅ API Documentation  

---

## Status

✅ Backend - COMPLETE  
✅ Frontend - COMPLETE  
✅ Docker - COMPLETE  
✅ Docs - COMPLETE  
✅ Production Ready - YES  

---

## Quick Start Order

1. Read GETTING_STARTED.md (5 min)
2. Run `docker-compose up` (1 min)
3. Visit http://localhost:3000 (instant)
4. Upload image and test (2 min)
5. Read remaining docs as needed

---

**Version**: 1.0.0 | **Status**: ✅ Ready | **Updated**: April 2024

Made with ♻️ for Earth 🌍
