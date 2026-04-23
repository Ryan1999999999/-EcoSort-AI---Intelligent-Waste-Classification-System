# 🚀 EcoSort AI - Getting Started Guide

## ⚡ 5-Minute Quick Start

### Prerequisites
- Docker & Docker Compose OR
- Python 3.9+ & Node.js 18+

### Fast Setup (Docker)
```bash
# Build all services
docker-compose -f docker/docker-compose.yml build

# Start all services  
docker-compose -f docker/docker-compose.yml up -d

# Access:
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Verify Services
```bash
docker-compose -f docker/docker-compose.yml ps
# Should show 3 healthy services
```

## 🛠️ Local Development Setup

### Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn app.main:app --reload --port 8000
```

Access API docs at: http://localhost:8000/docs

### Frontend (Terminal 2)

```bash
# Navigate to frontend  
cd frontend

# Install npm packages
npm install

# Start dev server
npm run dev
```

Access web app at: http://localhost:5173

## 📖 Complete Documentation

After quick start, read these in order:

| Document | Purpose |
|----------|---------|
| [DEVELOPMENT.md](./docs/DEVELOPMENT.md) | Complete development guide |
| [BACKEND.md](./docs/BACKEND.md) | API routes & configuration |
| [FRONTEND.md](./docs/FRONTEND.md) | Vue.js components & setup |
| [DEPLOYMENT.md](./docs/DEPLOYMENT.md) | Production & Docker setup |

## 🎯 What to Try First

1. **Upload an Image**
   - Go to http://localhost:3000/classify
   - Drag & drop a waste image
   - See real-time classification

2. **View API Docs**
   - Go to http://localhost:8000/docs
   - Try the `/predict` endpoint
   - Send a test image

3. **Check Metrics**
   - Go to http://localhost:3000/metrics
   - See prediction history
   - View performance statistics

## 🔑 Key Features

✅ **Backend**
- FastAPI REST API
- ONNX model inference
- Pydantic v2 validation
- CORS support
- Health checks

✅ **Frontend**
- Vue.js 3 + TypeScript
- Vite build tool
- Drag & drop upload
- Real-time results
- Classification history

✅ **Docker**
- Multi-stage builds
- Health checks
- Networking
- Volume management

## 📊 API Endpoints Quick Reference

```bash
# Health check
curl http://localhost:8000/health

# Get model info
curl http://localhost:8000/model/info

# Get waste classes
curl http://localhost:8000/classes

# Make prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@image.jpg"
```

## 🐛 Quick Troubleshooting

**Backend won't start?**
```bash
# Check if port 8000 is available
lsof -i :8000
# Kill if needed: kill -9 <PID>
```

**Frontend can't connect to backend?**
```bash
# Check CORS in backend/app/main.py
# Update if needed to include http://localhost:5173
```

**Docker build fails?**
```bash
# Clean up and rebuild
docker system prune -a
docker-compose build --no-cache
```

## 📦 Project Structure Summary

```
EcoSort-AI/
├── backend/          ← FastAPI API (port 8000)
├── frontend/         ← Vue.js web app (port 5173/3000)
├── docker/           ← Docker configs
├── models/           ← ONNX model (314MB)
├── docs/             ← Documentation
└── README.md         ← Main README
```

## ✅ Next Steps

1. ✅ Run backend & frontend locally
2. ✅ Upload test images
3. ✅ Read detailed documentation
4. ✅ Try Docker deployment
5. ✅ Deploy to production

## 🎓 Learning Path

**Beginner:**
1. Run quick start
2. Use web interface
3. Read this guide

**Intermediate:**
1. Read BACKEND.md
2. Read FRONTEND.md
3. Run locally
4. Customize components

**Advanced:**
1. Read DEPLOYMENT.md
2. Deploy with Docker
3. Configure production
4. Set up monitoring

## 📞 Need Help?

- 📖 Check relevant documentation in `/docs`
- 🐛 See troubleshooting sections
- 💬 API docs at `/docs` endpoint
- 🔍 Check logs: `docker-compose logs`

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: April 2024
