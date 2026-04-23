# EcoSort AI - Full Deployment Guide

## 🎯 Overview

Complete setup instructions for deploying EcoSort AI with Docker, containing:
- FastAPI Backend (Port 8000)
- Vue.js 3 Frontend (Port 80/3000)
- Optional MLflow Server (Port 5000)

## 📋 Prerequisites

### System Requirements
- Docker & Docker Compose installed
- 4GB RAM minimum
- 2GB disk space

### Software Versions
- Docker: 20.10+
- Docker Compose: 2.0+
- Python: 3.9+ (for local development)
- Node.js: 18+ (for local development)

### Check Installation

```bash
docker --version
docker-compose --version
```

## 🚀 Quick Start (Docker)

### 1. Prepare Model

Ensure `models/best_model.onnx` exists:
```bash
ls -lh models/best_model.onnx
# Should show the 314MB ONNX model
```

### 2. Build All Services

```bash
cd docker
docker-compose build
```

Expected output:
```
Building backend
...
Building frontend
...
Building mlflow
...
```

### 3. Start All Services

```bash
docker-compose up -d
```

Expected output:
```
Creating ecosort-backend  ... done
Creating ecosort-frontend ... done
Creating ecosort-mlflow   ... done
```

### 4. Verify Services

```bash
docker-compose ps
```

Should show 3 services running:
```
NAME              STATUS              PORTS
ecosort-backend   Up (healthy)        0.0.0.0:8000->8000/tcp
ecosort-frontend  Up (healthy)        0.0.0.0:80->80/tcp, 0.0.0.0:3000->80/tcp
ecosort-mlflow    Up                  0.0.0.0:5000->5000/tcp
```

## 🌐 Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Web application |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **MLflow** | http://localhost:5000 | Experiment tracking |

## 🛠️ Local Development (Without Docker)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload --port 8000
```

Access API at: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Access frontend at: http://localhost:5173

## 📊 API Endpoints

### Health Check
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

### Make Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@image.jpg"
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
  "impact_message": "..."
}
```

### Get Model Info
```bash
curl http://localhost:8000/model/info
```

### Get Waste Classes
```bash
curl http://localhost:8000/classes
```

## 🔍 Troubleshooting

### Issue: Backend Container Fails to Start

```bash
# Check logs
docker-compose logs backend

# Verify model exists
ls -lh models/best_model.onnx
```

**Solution:** Ensure ONNX model is in `models/` directory

### Issue: Frontend Can't Connect to Backend

Update `frontend/.env`:
```env
VITE_API_URL=http://backend:8000
```

Or use API proxy in docker-compose

### Issue: Port 80 Already in Use

Change frontend port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8080:80"  # Changed from 80 to 8080
```

Then access at http://localhost:8080

### Issue: Out of Disk Space

```bash
# Remove unused images
docker image prune

# Remove stopped containers
docker container prune

# View disk usage
docker system df
```

## 🔐 Production Deployment

### Environment Setup

Create `.env.production`:
```env
# Backend
BACKEND_HOST=api.yourdomain.com
BACKEND_PORT=8000
ENV=production

# Frontend
FRONTEND_HOST=yourdomain.com
VITE_API_URL=https://api.yourdomain.com

# Security
CORS_ORIGINS=["https://yourdomain.com"]
```

### SSL/HTTPS Setup

1. **Install Certbot:**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Generate Certificate:**
   ```bash
   sudo certbot certonly --standalone -d yourdomain.com
   ```

3. **Update Nginx Configuration:**
   ```nginx
   server {
       listen 443 ssl http2;
       server_name yourdomain.com;
       
       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
       
       # ... rest of config
   }
   ```

### Database Backup

```bash
# Backup volumes
docker run --rm -v mlflow-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/mlflow-backup.tar.gz -C /data .
```

### Monitoring

Check resource usage:
```bash
docker stats
```

View logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mlflow
```

## 📈 Performance Optimization

### Backend

1. **Use GPU Acceleration** (optional):
   ```bash
   # Install NVIDIA Docker runtime
   docker-compose exec backend python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
   ```

2. **Enable Caching:**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1)
   def load_model():
       return WasteClassifier()
   ```

### Frontend

1. **Enable Compression:**
   - Already configured in `docker/nginx.conf`
   - Gzip enabled for CSS, JS, JSON

2. **Cache Optimization:**
   - Static assets cached for 1 year
   - Index.html not cached (reload on deploy)

## 🚀 Scaling

### Horizontal Scaling

Run multiple backend instances with load balancer:

```yaml
services:
  backend-1:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8001:8000"
  
  backend-2:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8002:8000"
  
  nginx-lb:
    image: nginx:alpine
    ports:
      - "8000:8000"
    volumes:
      - ./docker/nginx-lb.conf:/etc/nginx/nginx.conf:ro
```

### Vertical Scaling

Increase resource limits in docker-compose:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build & Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker images
        run: docker-compose build
      
      - name: Push to registry
        run: |
          docker tag ecosort-backend:latest ${{ secrets.REGISTRY_URL }}/ecosort-backend
          docker push ${{ secrets.REGISTRY_URL }}/ecosort-backend
```

## 📝 Logging Configuration

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend

# Follow logs
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Log Files Inside Container

```bash
# Backend logs
docker exec ecosort-backend cat /var/log/app.log

# Frontend errors
docker exec ecosort-frontend cat /var/log/nginx/error.log
```

## 🛑 Stop & Cleanup

### Stop All Services

```bash
docker-compose down
```

### Stop & Remove Volumes

```bash
docker-compose down -v
```

### Remove Everything

```bash
docker-compose down -v
docker system prune -a
```

## 📊 System Architecture

```
                           ┌─────────────────────┐
                           │   User's Browser    │
                           └──────────┬──────────┘
                                      │
                           ┌──────────┴──────────┐
                           │   Nginx Reverse     │
                           │   Proxy (Port 80)   │
                           └────────┬─────┬──────┘
                                    │     │
                     ┌──────────────┘     └──────────────┐
                     │                                    │
              ┌──────▼────────┐                ┌──────────▼──────┐
              │   Frontend    │                │    Backend API  │
              │   (Vue.js 3)  │                │   (FastAPI)     │
              │   Port 80     │                │   Port 8000     │
              └───────────────┘                └────────┬────────┘
                                                        │
                                              ┌─────────▼────────┐
                                              │  ONNX Runtime    │
                                              │  Model Inference │
                                              └──────────────────┘

                                       ┌────────────────────────┐
                                       │  Optional: MLflow      │
                                       │  Tracking Server       │
                                       │  Port 5000             │
                                       └────────────────────────┘
```

## 📞 Support & Documentation

- **Backend Docs**: See [BACKEND.md](../docs/BACKEND.md)
- **Frontend Docs**: See [FRONTEND.md](../docs/FRONTEND.md)
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Project README**: See [README.md](../README.md)

## ✅ Deployment Checklist

- [ ] Model file exists at `models/best_model.onnx`
- [ ] Docker and Docker Compose installed
- [ ] All services build without errors
- [ ] Services start and pass health checks
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend API accessible at http://localhost:8000
- [ ] API docs available at http://localhost:8000/docs
- [ ] Can make predictions successfully
- [ ] No CORS errors in browser console
- [ ] Environment variables configured correctly

## 🎉 Next Steps

1. ✅ Complete local setup
2. ✅ Test all endpoints
3. ✅ Configure SSL for production
4. ✅ Set up monitoring & logging
5. ✅ Deploy to cloud platform (AWS, GCP, Azure, etc.)
