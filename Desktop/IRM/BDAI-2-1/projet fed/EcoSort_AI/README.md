# EcoSort AI - Intelligent Waste Classification System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![ONNX](https://img.shields.io/badge/ONNX-0055FF?style=for-the-badge)

**EcoSort AI** is an intelligent waste classification system that uses deep learning to automatically identify and categorize recyclable materials. The system aims to help recycling facilities improve sorting accuracy, reduce contamination, and increase recycling rates.

## 🎯 Project Goals

- Achieve **≥ 89%** accuracy in classifying 6 types of waste
- Build a production-ready FastAPI backend with real-time inference
- Develop a modern, user-friendly Vue.js frontend
- Track experiments using MLflow
- Demonstrate measurable environmental impact

## 📊 Model Performance

- **Best Model**: MobileNetV3 Large  
- **Validation Accuracy**: **92.88%**  
- **Dataset**: TrashNet (2,527 images)  
- **Classes**: Cardboard, Glass, Metal, Paper, Plastic, Trash

## 🛠️ Technology Stack

### Backend
- **FastAPI** + Uvicorn
- **ONNX Runtime** (optimized inference)
- PyTorch + TIMM (training)
- Albumentations (data augmentation)
- MLflow (experiment tracking)

### Frontend
- **Vue.js 3** + TypeScript
- **Vite** (build tool)
- **Element Plus** (UI components)
- **Axios** (API calls)
- **Chart.js** (data visualization)

### DevOps & Deployment
- Docker + Docker Compose
- Nginx (reverse proxy)
- Git + GitHub

## 📁 Project Structure

```bash
EcoSort-AI/
├── notebooks/                  # Kaggle training experiments
├── models/                     # Trained models (best_model.onnx)
├── backend/                    # FastAPI REST API
├── frontend/                   # Vue.js 3 Web Interface
├── docker/                     # Docker configuration
├── docs/
├── .gitignore
├── README.md
└── requirements.txt