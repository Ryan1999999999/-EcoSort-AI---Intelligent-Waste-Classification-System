<template>
  <div class="home-page">
    <el-row :gutter="20" class="mb-30">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card class="hero-card">
          <div class="hero-content">
            <h1 class="hero-title">♻️ EcoSort AI</h1>
            <p class="hero-subtitle">Intelligent Waste Classification System</p>
            <p class="hero-description">
              Powered by deep learning, EcoSort AI automatically identifies and categorizes recyclable materials
              to help recycling facilities improve sorting accuracy and increase recycling rates.
            </p>
            <el-button type="success" size="large" @click="navigateToClassify" round>
              Start Classifying →
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>📊 Model Performance</span>
            </div>
          </template>
          <el-statistic title="Validation Accuracy" :value="92.88" suffix="%" size="large"></el-statistic>
          <el-divider></el-divider>
          <el-statistic title="Supported Classes" :value="6"></el-statistic>
          <el-divider></el-divider>
          <el-statistic title="Training Dataset" :value="'TrashNet (2,527 images)'"></el-statistic>
          <el-divider></el-divider>
          <el-statistic title="Model" :value="'MobileNetV3 Large (ONNX)'"></el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <!-- Features Section -->
    <el-row :gutter="20" class="mb-30">
      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <el-card class="feature-card">
          <div class="feature-icon">🖼️</div>
          <h3>Image Upload</h3>
          <p>Drag and drop or upload waste images for instant classification</p>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <el-card class="feature-card">
          <div class="feature-icon">⚡</div>
          <h3>Real-time Inference</h3>
          <p>Get predictions in milliseconds with confidence scores</p>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <el-card class="feature-card">
          <div class="feature-icon">🌍</div>
          <h3>Impact Tracking</h3>
          <p>Learn environmental impact of each waste category</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- Waste Classes -->
    <el-card class="mb-30">
      <template #header>
        <div class="card-header">
          <span>🗑️ Waste Categories</span>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :xs="12" :sm="12" :md="6" :lg="4" v-for="(name, key) in classes" :key="key" class="mb-20">
          <div class="class-box">
            <div class="class-emoji">{{ getClassEmoji(name) }}</div>
            <h4>{{ formatClassName(name) }}</h4>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- Info Section -->
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-alert
          title="ℹ️ How It Works"
          type="info"
          :closable="false"
          description="Upload a waste image, and our AI model will instantly classify it into one of 6 categories with confidence scores. Each prediction includes environmental impact information to help you understand the importance of proper recycling."
          show-icon
        ></el-alert>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-alert
          title="🔧 Technology Stack"
          type="success"
          :closable="false"
          description="Built with Vue.js 3, FastAPI, ONNX Runtime, and MobileNetV3. Optimized for fast inference on CPU."
          show-icon
        ></el-alert>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { predictionAPI } from '@/api/client'

const router = useRouter()
const classes = ref<{ [key: number]: string }>({})

const classEmojiMap: { [key: string]: string } = {
  'cardboard': '📦',
  'glass': '🍾',
  'metal': '🔗',
  'paper': '📄',
  'plastic': '🥤',
  'trash': '🗑️'
}

const getClassEmoji = (className: string): string => {
  return classEmojiMap[className] || '📌'
}

const formatClassName = (name: string): string => {
  return name.charAt(0).toUpperCase() + name.slice(1)
}

const navigateToClassify = () => {
  router.push('/classify')
}

onMounted(async () => {
  try {
    const response = await predictionAPI.getClasses()
    classes.value = response.data.classes
  } catch (error) {
    console.error('Failed to load classes:', error)
  }
})
</script>

<style scoped lang="css">
.home-page {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.mb-30 {
  margin-bottom: 30px;
}

.mb-20 {
  margin-bottom: 20px;
}

.hero-card :deep(.el-card__body) {
  padding: 40px;
}

.hero-content {
  text-align: center;
}

.hero-title {
  font-size: 48px;
  color: #2c3e50;
  margin-bottom: 15px;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 24px;
  color: #34495e;
  margin-bottom: 20px;
  font-weight: 500;
}

.hero-description {
  font-size: 16px;
  color: #555;
  margin-bottom: 30px;
  line-height: 1.6;
}

.stats-card {
  height: 100%;
}

.stats-card :deep(.el-statistic__content) {
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
}

.feature-card {
  height: 100%;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.feature-card h3 {
  margin: 15px 0 10px 0;
  color: #2c3e50;
  font-size: 18px;
}

.feature-card p {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.class-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  color: white;
  transition: all 0.3s ease;
  cursor: pointer;
}

.class-box:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.class-emoji {
  font-size: 40px;
  margin-bottom: 10px;
}

.class-box h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

:deep(.el-alert) {
  margin-bottom: 0;
}

:deep(.el-divider) {
  margin: 15px 0;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-description {
    font-size: 14px;
  }
}
</style>
