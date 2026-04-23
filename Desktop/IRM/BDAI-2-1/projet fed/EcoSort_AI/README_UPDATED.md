# Update the main README with deployment information
# This is the updated README.md

# EcoSort AI - Intelligent Waste Classification System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![ONNX](https://img.shields.io/badge/ONNX-0055FF?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**EcoSort AI** is a production-ready intelligent waste classification system that uses deep learning to automatically identify and categorize recyclable materials. The system helps recycling facilities improve sorting accuracy, reduce contamination, and increase recycling rates.

## 🎯 Project Goals

- Achieve **≥ 89%** accuracy in classifying 6 types of waste ✅ **92.88% achieved**
- Build a production-ready FastAPI backend with real-time inference ✅ **Complete**
- Develop a modern, user-friendly Vue.js 3 frontend ✅ **Complete**
- Track experiments using MLflow
- Demonstrate measurable environmental impact ✅ **Integrated**
- Easy deployment with Docker & Docker Compose ✅ **Complete**

## 📊 Model Performance

- **Best Model**: MobileNetV3 Large  
- **Validation Accuracy**: **92.88%**  
- **Dataset**: TrashNet (2,527 images)  
- **Classes**: Cardboard, Glass, Metal, Paper, Plastic, Trash
- **Inference Time**: ~50-100ms per image (CPU)
- **Model Size**: 314MB (ONNX format)

## 🛠️ Technology Stack

### Backend
- **FastAPI** + Uvicorn
- **ONNX Runtime** (optimized inference)
- **Pydantic v2** (data validation)
- PyTorch + TIMM (training)
- Albumentations (data augmentation)

### Frontend
- **Vue.js 3** + TypeScript
- **Vite** (build tool)
- **Element Plus** (UI components)
- **Pinia** (state management)
- **Axios** (HTTP client)
- **Chart.js** (data visualization)

### DevOps & Deployment
- **Docker** + **Docker Compose**
- **Nginx** (reverse proxy & static file serving)
- **Git** + GitHub

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Or Python 3.9+ and Node.js 18+ for local development

### Option 1: Docker (Recommended)
```bash
# Build all services
docker-compose -f docker/docker-compose.yml build

# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
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

# Terminal 2: Frontend (new terminal)
cd frontend
npm install
npm run dev

# Open http://localhost:5173
```

## 📚 Documentation

- **[DEVELOPMENT.md](./docs/DEVELOPMENT.md)** - Complete development guide
- **[BACKEND.md](./docs/BACKEND.md)** - Backend API documentation & setup
- **[FRONTEND.md](./docs/FRONTEND.md)** - Frontend development guide
- **[DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Docker deployment & production setup
- **[PROJECT_SUMMARY.md](./docs/PROJECT_SUMMARY.md)** - Detailed project overview

## 🌐 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check & model status |
| `/model/info` | GET | Model information & metrics |
| `/classes` | GET | Available waste classes |
| `/predict` | POST | Classify waste image |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

## 📸 Web Interface

### Pages
1. **Home** - Project overview & statistics
2. **Classify** - Drag & drop image upload with real-time results
3. **Metrics** - Model performance charts & classification history
4. **Impact** - Environmental impact tracking & waste information

## 📁 Project Structure

```bash
EcoSort-AI/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py            # API routes & startup
│   │   ├── core/inference.py  # ONNX inference engine
│   │   ├── models/schemas.py  # Pydantic models
│   │   └── utils/             # Utilities
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # Vue.js 3 + Vite
│   ├── src/
│   │   ├── views/             # Page components
│   │   ├── api/               # API client
│   │   ├── stores/            # Pinia state
│   │   └── router/            # Vue Router
│   ├── package.json
│   └── .env.example
│
├── docker/                     # Container configuration
│   ├── docker-compose.yml      # Service orchestration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
│
├── models/
│   └── best_model.onnx         # Trained model (314MB)
│
├── notebooks/
│   └── 01_trashnet_training.ipynb
│
├── docs/
│   ├── BACKEND.md
│   ├── FRONTEND.md
│   ├── DEPLOYMENT.md
│   ├── DEVELOPMENT.md
│   └── PROJECT_SUMMARY.md
│
└── README.md
```

## 🔌 API Usage Example

```python
import requests

# Make prediction
response = requests.post(
    'http://localhost:8000/predict',
    files={'file': open('waste_image.jpg', 'rb')}
)

result = response.json()
print(f"Class: {result['predicted_class']}")
print(f"Confidence: {result['confidence']}%")
print(f"Impact: {result['impact_message']}")
```

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run lint
npm run type-check
```

## 🐳 Docker Commands

```bash
# Build services
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## 📊 Service URLs

| Service | URL | Port |
|---------|-----|------|
| Frontend | http://localhost:3000 | 3000 |
| Backend API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |
| MLflow (Optional) | http://localhost:5000 | 5000 |

## 🔐 Security Features

- ✅ CORS support with configurable origins
- ✅ File size validation (10MB limit)
- ✅ Input type checking
- ✅ Error handling with meaningful messages
- ✅ Request validation with Pydantic
- ✅ HTTPS support in production
- ✅ Environment-based configuration

## 📈 Performance

- **Backend**: ~50-100ms per prediction (CPU)
- **Frontend**: <100ms response time
- **Model Size**: 314MB (ONNX)
- **Memory Usage**: ~300MB
- **Throughput**: 10+ predictions/second (CPU)

## 🌍 Environmental Impact

Each waste classification helps:
- 🌳 **Cardboard**: Saves 5 liters of water per item
- 🔗 **Metal**: Uses 95% less energy than mining
- 🥤 **Plastic**: Prevents 400+ years of decomposition
- ♻️ **Glass**: 100% recyclable without degradation
- 📄 **Paper**: Reduces deforestation
- 🗑️ **Trash**: Minimizes landfill waste

## 🚀 Deployment

### Local Development
```bash
# See DEVELOPMENT.md
```

### Docker Deployment
```bash
# See DEPLOYMENT.md for complete instructions
docker-compose up
```

### Production
1. Configure SSL/HTTPS
2. Set environment variables
3. Use cloud hosting (AWS, GCP, Azure, etc.)
4. Set up monitoring & logging
5. Configure backups

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed steps.

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- TrashNet dataset creators
- FastAPI & Vue.js communities
- ONNX Runtime developers
- Element Plus UI library

## 📞 Support

For issues and questions:
- 📖 Read the detailed documentation in `/docs`
- 🐛 Check troubleshooting sections in relevant docs
- 💬 Review API documentation at `/docs` endpoint

---

## 📊 Project Statistics

- **Backend Lines of Code**: ~400
- **Frontend Lines of Code**: ~1000
- **Documentation Pages**: 5
- **API Endpoints**: 4
- **Frontend Pages**: 4
- **Model Accuracy**: 92.88%
- **Dev Time**: Progressive phases
- **Status**: ✅ Production Ready

---

**Created**: 2024  
**Last Updated**: April 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✅

Made with ♻️ for a sustainable future
