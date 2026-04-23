# PROJECT SUMMARY - EcoSort AI

**Intelligent Waste Classification System using Deep Learning**

**Submitted by:** Rayen Sghairi  
**Course:** BDAI-2-1  

## 1. Project Overview

EcoSort AI is an AI-powered waste classification system designed to automatically identify and categorize recyclable materials. The system aims to assist industrial recycling facilities by improving sorting accuracy, reducing contamination rates, and increasing the overall recycling rate.

**Target Improvement:**
- Current manual sorting contamination rate: **15%**
- Target contamination rate with AI: **≤ 5%**
- Expected recycling rate increase: from **35% to 60%**

## 2. Problem Statement

- Manual sorting is labor-intensive, dangerous, and inaccurate
- High contamination rate (15%) leads to recyclable materials being sent to landfills
- Human sorters work in hazardous conditions with low efficiency
- Misclassification causes significant economic and environmental loss

## 3. Solution

An end-to-end deep learning system that:
- Takes an image of waste as input
- Classifies it into one of 6 categories with high confidence
- Provides recycling advice and environmental impact estimation
- Runs in real-time (< 50ms per item)

## 4. Dataset

- **Dataset Name**: TrashNet
- **Total Images**: 2,527
- **Image Resolution**: 512×384
- **Classes** (6 classes):

  | Class          | Number of Images |
  |----------------|------------------|
  | Paper          | 594              |
  | Glass          | 501              |
  | Plastic        | 482              |
  | Metal          | 410              |
  | Cardboard      | 403              |
  | Trash          | 137              |

- **Split**: 70% Train / 15% Validation / 15% Test (stratified)

## 5. Methodology

### 5.1 Model Architectures Compared
- EfficientNetV2 (rw_s)
- ResNet50
- MobileNetV3 Large
- InceptionV3

### 5.2 Training Details
- Framework: PyTorch + TIMM
- Data Augmentation: Albumentations (HorizontalFlip, ShiftScaleRotate, RandomBrightnessContrast, etc.)
- Optimizer: AdamW
- Loss: CrossEntropyLoss
- Image Size: 320×320
- Batch Size: 16
- Training done on Kaggle GPU (Tesla T4)

### 5.3 Best Model Performance

| Model                  | Validation Accuracy | Best Epoch |
|------------------------|---------------------|------------|
| MobileNetV3 Large      | **92.88%**          | 8          |
| ResNet50               | 92.35%              | -          |
| EfficientNetV2         | 91.56%              | -          |
| InceptionV3            | 83.64%              | -          |

**Final Chosen Model**: MobileNetV3 Large (92.88% accuracy)

## 6. Model Export

- Best model exported to **ONNX** format for fast inference
- Used ONNX Runtime for production deployment

## 7. Planned Architecture

- **Backend**: FastAPI + ONNX Runtime
- **Frontend**: Vue.js 3 + TypeScript + Element Plus
- **Deployment**: Docker + Docker Compose
- **MLOps**: MLflow for experiment tracking

## 8. Expected Features

- Drag & drop image upload
- Real-time classification with confidence score
- Recycling guidance per material
- Environmental impact visualization (CO₂ saved)
- Model performance dashboard

## 9. Future Improvements

- Implement data augmentation techniques (MixUp, CutMix)
- Hyperparameter tuning using Optuna
- Add batch prediction support
- Deploy the system on cloud platform
- Integrate with real industrial sorting cameras

## 10. Conclusion

EcoSort AI demonstrates the potential of deep learning in solving real-world environmental challenges. With a validation accuracy of **92.88%**, the system significantly outperforms manual sorting and provides a scalable solution for modern recycling facilities.

---

**Status**: Training Phase Completed | Backend Development In Progress

