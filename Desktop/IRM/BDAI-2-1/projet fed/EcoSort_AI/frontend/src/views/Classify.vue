<template>
  <div class="classify-page">
    <el-row :gutter="20">
      <!-- Upload Section -->
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card class="upload-card">
          <template #header>
            <div class="card-header">
              <span>📸 Upload Image</span>
            </div>
          </template>

          <div class="upload-area" @dragover.prevent="dragOver = true" @dragleave.prevent="dragOver = false" @drop.prevent="handleDrop">
            <input
              type="file"
              ref="fileInput"
              accept="image/*"
              style="display: none"
              @change="handleFileSelect"
            />

            <div v-if="!preview" class="upload-placeholder" :class="{ 'drag-over': dragOver }">
              <div class="upload-icon">🖼️</div>
              <p class="upload-text">Drag and drop your image here</p>
              <p class="upload-sub-text">or</p>
              <el-button type="primary" @click="selectFile">Choose Image</el-button>
              <p class="upload-format">Supported: JPG, PNG</p>
            </div>

            <div v-else class="preview-container">
              <img :src="preview" class="preview-image" />
              <el-button type="danger" @click="clearPreview" plain>Clear Image</el-button>
            </div>
          </div>

          <el-button
            v-if="preview"
            type="success"
            @click="predict"
            :loading="loading"
            class="predict-btn"
            size="large"
            round
          >
            🔍 Classify Waste
          </el-button>
        </el-card>
      </el-col>

      <!-- Results Section -->
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card class="results-card">
          <template #header>
            <div class="card-header">
              <span>📊 Classification Results</span>
            </div>
          </template>

          <div v-if="!currentResult && !error" class="empty-state">
            <p class="empty-text">Upload an image to see results</p>
          </div>

          <div v-else-if="error" class="error-state">
            <el-alert :title="error" type="error" :closable="false" show-icon></el-alert>
          </div>

          <div v-else-if="currentResult" class="result-state">
            <!-- Predicted Class -->
            <div class="result-header">
              <div class="result-class-emoji">{{ getClassEmoji(currentResult.predicted_class) }}</div>
              <div class="result-class-info">
                <h2 class="result-class">{{ formatClassName(currentResult.predicted_class) }}</h2>
                <p class="result-confidence">Confidence: <strong>{{ currentResult.confidence }}%</strong></p>
              </div>
            </div>

            <el-divider></el-divider>

            <!-- Impact Message -->
            <div class="impact-section">
              <h3>🌍 Environmental Impact</h3>
              <p class="impact-message">{{ currentResult.impact_message }}</p>
            </div>

            <el-divider></el-divider>

            <!-- All Scores -->
            <div class="scores-section">
              <h3>📈 Confidence Scores</h3>
              <div v-for="(score, className) in currentResult.all_scores" :key="className" class="score-item">
                <div class="score-label">
                  <span class="score-emoji">{{ getClassEmoji(className) }}</span>
                  <span class="score-name">{{ formatClassName(className) }}</span>
                </div>
                <el-progress
                  :percentage="score"
                  :color="getScoreColor(score)"
                  class="score-bar"
                ></el-progress>
                <span class="score-value">{{ score }}%</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons">
              <el-button @click="clearResults" plain>Clear Results</el-button>
              <el-button type="primary" @click="selectFile">Classify Another</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- History Section -->
    <el-card class="history-card" v-if="predictions.length > 0">
      <template #header>
        <div class="card-header">
          <span>📜 Classification History ({{ predictions.length }})</span>
          <el-button type="danger" @click="clearHistory" text>Clear All</el-button>
        </div>
      </template>

      <el-table :data="predictions" stripe style="width: 100%">
        <el-table-column prop="predicted_class" label="Class" width="150">
          <template #default="{ row }">
            <span class="history-class">{{ getClassEmoji(row.predicted_class) }} {{ formatClassName(row.predicted_class) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="confidence" label="Confidence" width="120" sortable>
          <template #default="{ row }">
            <el-progress
              :percentage="row.confidence"
              :color="getScoreColor(row.confidence)"
              :show-text="false"
              style="width: 100%; margin-right: 10px"
            ></el-progress>
            {{ row.confidence }}%
          </template>
        </el-table-column>
        <el-table-column prop="top_class" label="Top Class" width="200">
          <template #default="{ row }">
            <span v-for="(score, className) in getTopClasses(row.all_scores, 3)" :key="className" class="badge">
              {{ formatClassName(className) }}: {{ score }}%
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { usePredictionStore } from '@/stores/predictionStore'
import { predictionAPI } from '@/api/client'

interface ClassificationResult {
  predicted_class: string
  confidence: number
  all_scores: { [key: string]: number }
  impact_message: string
}

const store = usePredictionStore()

const fileInput = ref<HTMLInputElement>()
const preview = ref<string>('')
const loading = ref(false)
const dragOver = ref(false)
const currentResult = ref<ClassificationResult | null>(null)
const error = ref<string>('')

const predictions = computed(() => store.predictions)

const classEmojiMap: { [key: string]: string } = {
  'cardboard': '📦',
  'glass': '🍾',
  'metal': '🔗',
  'paper': '📄',
  'plastic': '🥤',
  'trash': '🗑️'
}

const selectFile = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    loadPreview(file)
  }
}

const handleDrop = (event: DragEvent) => {
  dragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file && file.type.startsWith('image/')) {
    loadPreview(file)
  } else {
    ElMessage.error('Please drop an image file')
  }
}

const loadPreview = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    preview.value = e.target?.result as string
    fileInput.value!.files = new DataTransfer().items.files // Reset file input
  }
  reader.readAsDataURL(file)
}

const predict = async () => {
  if (!preview.value) {
    ElMessage.error('Please select an image')
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Convert preview to File
    const response = await fetch(preview.value)
    const blob = await response.blob()
    const file = new File([blob], 'image.jpg', { type: 'image/jpeg' })

    const result = await predictionAPI.predict(file)
    currentResult.value = result.data
    store.addPrediction(result.data)
    ElMessage.success('Classification complete!')
  } catch (err: any) {
    const message = err.response?.data?.detail || 'Classification failed. Please try again.'
    error.value = message
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

const clearPreview = () => {
  preview.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const clearResults = () => {
  currentResult.value = null
  error.value = ''
}

const clearHistory = () => {
  store.clearPredictions()
}

const getClassEmoji = (className: string): string => {
  return classEmojiMap[className] || '📌'
}

const formatClassName = (name: string): string => {
  return name.charAt(0).toUpperCase() + name.slice(1)
}

const getScoreColor = (score: number): string => {
  if (score >= 80) return '#67c23a'
  if (score >= 60) return '#e6a23c'
  if (score >= 40) return '#f56c6c'
  return '#909399'
}

const getTopClasses = (scores: { [key: string]: number }, limit: number): string[] => {
  return Object.entries(scores)
    .sort(([, a], [, b]) => b - a)
    .slice(0, limit)
    .map(([name, score]) => `${name}: ${score.toFixed(1)}%`)
}
</script>

<style scoped lang="css">
.classify-page {
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

.upload-card, .results-card {
  min-height: 600px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  transition: all 0.3s ease;
  min-height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.upload-area.drag-over {
  border-color: #409eff;
  background: rgba(64, 158, 255, 0.1);
}

.upload-placeholder {
  width: 100%;
}

.upload-icon {
  font-size: 64px;
  margin-bottom: 15px;
}

.upload-text {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
  font-weight: 500;
}

.upload-sub-text {
  color: #999;
  font-size: 14px;
  margin: 10px 0;
}

.upload-format {
  color: #bbb;
  font-size: 12px;
  margin-top: 15px;
}

.preview-container {
  width: 100%;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  margin-bottom: 15px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.predict-btn {
  width: 100% !important;
  font-size: 16px;
  height: 40px;
}

.empty-state, .error-state {
  padding: 40px 20px;
  text-align: center;
  color: #999;
}

.empty-text {
  font-size: 16px;
  margin: 0;
}

.result-state {
  padding: 20px 0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.result-class-emoji {
  font-size: 64px;
}

.result-class {
  margin: 0;
  color: #2c3e50;
  font-size: 28px;
  font-weight: 700;
}

.result-confidence {
  margin: 5px 0 0 0;
  color: #666;
  font-size: 16px;
}

.impact-section {
  margin-bottom: 20px;
}

.impact-section h3 {
  color: #2c3e50;
  font-size: 16px;
  margin-bottom: 10px;
}

.impact-message {
  background: #e8f5e9;
  padding: 15px;
  border-left: 4px solid #67c23a;
  border-radius: 4px;
  color: #333;
  line-height: 1.6;
  margin: 0;
}

.scores-section {
  margin-bottom: 20px;
}

.scores-section h3 {
  color: #2c3e50;
  font-size: 16px;
  margin-bottom: 15px;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.score-label {
  flex-shrink: 0;
  width: 120px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-emoji {
  font-size: 20px;
}

.score-name {
  color: #666;
  font-size: 14px;
}

.score-bar {
  flex: 1 !important;
}

.score-value {
  flex-shrink: 0;
  width: 50px;
  text-align: right;
  color: #333;
  font-weight: 600;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.action-buttons .el-button {
  flex: 1;
}

.history-card {
  margin-top: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.history-class {
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  background: #f0f9ff;
  color: #0081ff;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 5px;
}

:deep(.el-progress) {
  margin: 0 10px 0 0;
}

@media (max-width: 768px) {
  .upload-area {
    min-height: 250px;
  }

  .result-header {
    flex-direction: column;
    text-align: center;
  }

  .result-class {
    font-size: 24px;
  }
}
</style>
