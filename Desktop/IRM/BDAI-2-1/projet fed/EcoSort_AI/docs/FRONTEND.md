# EcoSort AI - Frontend Setup Guide

## 📋 Overview

Modern Vue.js 3 + TypeScript frontend with Element Plus UI components for real-time waste classification.

## 🚀 Quick Start

### Step 1: Install Node.js

Ensure you have Node.js 16+ installed:
```bash
node --version  # Should be v16.0.0 or higher
npm --version
```

### Step 2: Install Dependencies

```bash
cd frontend
npm install
```

### Step 3: Configure Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit if necessary (defaults work for local development)
cat .env
```

**Default configuration:**
```env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=EcoSort AI
```

### Step 4: Start Development Server

```bash
npm run dev
```

Expected output:
```
  VITE v5.0.2  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Access the app at **http://localhost:5173**

## 📁 Frontend Structure

```
frontend/
├── src/
│   ├── components/           # Reusable Vue components
│   ├── views/               # Page components
│   │   ├── Home.vue         # Welcome page
│   │   ├── Classify.vue     # Main classification page
│   │   ├── Metrics.vue      # Performance metrics
│   │   └── Impact.vue       # Environmental impact
│   ├── api/
│   │   └── client.ts        # Axios API client
│   ├── stores/
│   │   └── predictionStore.ts # Pinia state management
│   ├── router/
│   │   └── index.ts         # Vue Router configuration
│   ├── App.vue              # Root component
│   └── main.ts              # Application entry point
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── .env.example
```

## 🎨 Pages & Features

### 1. **Home Page** (/) 
- Project overview
- Model performance statistics
- Waste categories showcase
- Quick navigation

### 2. **Classify Page** (/classify)
- Drag-and-drop image upload
- Real-time predictions
- Confidence scores for all classes
- Environmental impact messages
- Classification history

### 3. **Metrics Page** (/metrics)
- Model performance metrics
- Classification distribution
- Confidence analysis
- Top predictions table
- Statistical aggregations

### 4. **Impact Page** (/impact)
- Environmental impact information
- Waste category details
- UN SDG alignment
- Recycling rates by country
- Your personal impact summary

## 🔌 API Integration

### API Client Configuration

File: `src/api/client.ts`

```typescript
// Create predictions
const result = await predictionAPI.predict(file)

// Get model info
const info = await predictionAPI.getModelInfo()

// Check health
const health = await predictionAPI.getHealth()

// Get classes
const classes = await predictionAPI.getClasses()
```

### API Proxy Setup

The Vite dev server proxy forwards requests to backend:
```
http://localhost:5173/api/predict → http://localhost:8000/predict
```

## 📦 Build for Production

### Build Static Files

```bash
npm run build
```

This creates optimized build in `dist/` folder:
- Minified JavaScript/CSS
- Tree-shaking for unused code
- Image optimization
- ~150-200KB gzipped total

### Preview Production Build

```bash
npm run preview
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
cd ..
docker build -f docker/Dockerfile.frontend -t ecosort-frontend:latest .
```

### Run Container

```bash
docker run -p 3000:80 ecosort-frontend:latest
```

Access at **http://localhost:3000**

### With docker-compose

```bash
docker-compose -f docker/docker-compose.yml up frontend
```

## 🧪 Development Guide

### Add New Page

1. Create component in `src/views/MyPage.vue`
2. Add route in `src/router/index.ts`
3. Add menu item in `src/App.vue`

### Add New Component

```typescript
// File: src/components/MyComponent.vue
<template>
  <div class="my-component">
    <h3>My Component</h3>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<style scoped>
.my-component {
  padding: 20px;
}
</style>
```

### Use Pinia Store

```typescript
import { usePredictionStore } from '@/stores/predictionStore'

const store = usePredictionStore()

// Access state
console.log(store.predictions)
console.log(store.totalPredictions)

// Call actions
store.addPrediction(data)
store.clearPredictions()
```

### Make API Calls

```typescript
import { predictionAPI } from '@/api/client'

try {
  const response = await predictionAPI.predict(file)
  console.log(response.data)
} catch (error) {
  console.error('API Error:', error)
}
```

## ⚙️ Configuration

### Environment Variables

Edit `.env`:

```env
# API URL - change for production
VITE_API_URL=https://api.yourdomain.com

# App title
VITE_APP_TITLE=EcoSort AI
```

### TypeScript Settings

Edit `tsconfig.json`:
- `"strict": true` - Strict type checking
- `"exactOptionalPropertyTypes": true` - Type safety

### Vite Configuration

Edit `vite.config.ts`:
- Port: `server.port: 5173`
- Proxy settings for API
- Build optimization

## 🎨 Styling

### Color Scheme

- Primary: `#2c3e50` (Dark)
- Success: `#67c23a` (Green)
- Warning: `#e6a23c` (Orange)
- Error: `#f56c6c` (Red)
- Info: `#409eff` (Blue)

### Element Plus Theming

Customize in `src/main.ts`:

```typescript
app.use(ElementPlus, {
  locale: zhCn,
})
```

## 📊 Performance Optimization

Currently optimized:
- ✅ Code splitting by route
- ✅ Lazy loading images
- ✅ Tree-shaking unused code
- ✅ Gzip compression
- ✅ CSS minification
- ✅ Image optimization

## 🔍 Troubleshooting

### Issue: Cannot POST http://localhost:8000

**Solution:** Ensure backend is running:
```bash
# In another terminal
cd backend
python -m uvicorn app.main:app --reload
```

### Issue: Module not found errors

**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Port 5173 already in use

**Solution:**
```bash
npm run dev -- --port 5174
```

### Issue: CORS errors

**Solution:** Update backend CORS in `backend/app/main.py`:
```python
allow_origins=["http://localhost:5173"]
```

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| vue | 3.3.4 | Frontend framework |
| vite | 5.0.2 | Build tool |
| axios | 1.6.2 | HTTP client |
| element-plus | 2.4.2 | UI components |
| pinia | 2.1.6 | State management |
| vue-router | 4.2.5 | Client-side routing |

## 🚀 Next Steps

1. ✅ Frontend Setup Complete
2. ⏭️ Connect to Backend API
3. ⏭️ Deploy with Docker
4. ⏭️ Configure Nginx proxy

## 📖 Additional Resources

- [Vue.js 3 Docs](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Element Plus Components](https://element-plus.org/)
- [Pinia State Management](https://pinia.vuejs.org/)
- [Axios Documentation](https://axios-http.com/)
