<template>
  <div class="metrics-page">
    <!-- Model Performance Metrics -->
    <el-row :gutter="20" class="mb-30">
      <el-col :xs="24" :sm="12" :md="6" :lg="6" v-for="metric in modelMetrics" :key="metric.label">
        <el-card class="metric-card">
          <el-statistic :title="metric.label" :value="metric.value" :precision="metric.precision"></el-statistic>
          <p class="metric-subtitle">{{ metric.subtitle }}</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- Classification Distribution -->
    <el-row :gutter="20" class="mb-30">
      <el-col :xs="24" :md="24" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>📊 Classification Distribution</span>
            </div>
          </template>
          <div class="chart-container">
            <div v-if="totalPredictions > 0" class="distribution-grid">
              <div v-for="(count, className) in classificationStats" :key="className" class="distribution-item">
                <div class="distribution-emoji">{{ getClassEmoji(className) }}</div>
                <div class="distribution-info">
                  <h4>{{ formatClassName(className) }}</h4>
                  <p class="distribution-count">{{ count }} classifications</p>
                  <el-progress :percentage="getClassPercentage(count)" :show-text="false"></el-progress>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>No predictions yet. <router-link to="/classify">Make your first prediction!</router-link></p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="24" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>📈 Overall Statistics</span>
            </div>
          </template>
          <el-table :data="statsTable" stripe :show-header="true" style="width: 100%">
            <el-table-column label="Metric" prop="metric" width="200"></el-table-column>
            <el-table-column label="Value" prop="value" align="right"></el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- Confidence Analysis -->
    <el-card class="mb-30">
      <template #header>
        <div class="card-header">
          <span>🎯 Confidence Analysis</span>
        </div>
      </template>

      <el-row :gutter="20" v-if="totalPredictions > 0">
        <el-col :xs="24" :md="8">
          <el-statistic title="Average Confidence" :value="parseFloat(averageConfidence)" suffix="%" size="large"></el-statistic>
        </el-col>
        <el-col :xs="24" :md="8">
          <el-statistic title="High Confidence (≥90%)" :value="highConfidenceCount" size="large"></el-statistic>
        </el-col>
        <el-col :xs="24" :md="8">
          <el-statistic title="Low Confidence (<70%)" :value="lowConfidenceCount" size="large"></el-statistic>
        </el-col>
      </el-row>

      <div v-else class="empty-state">
        <p>No data available yet</p>
      </div>

      <!-- Confidence Histogram -->
      <div v-if="totalPredictions > 0" class="confidence-histogram mt-30">
        <h3>Confidence Distribution</h3>
        <div class="histogram-bars">
          <div v-for="range in confidenceRanges" :key="range.label" class="histogram-bar">
            <div class="bar-label">{{ range.label }}</div>
            <div class="bar-container">
              <div class="bar" :style="{ width: range.percentage + '%', backgroundColor: range.color }"></div>
            </div>
            <div class="bar-value">{{ range.count }}</div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- Top Predictions -->
    <el-card v-if="topPredictions.length > 0">
      <template #header>
        <div class="card-header">
          <span>⭐ Top Predictions (Highest Confidence)</span>
        </div>
      </template>

      <el-table :data="topPredictions" stripe style="width: 100%">
        <el-table-column type="index" label="#" width="50"></el-table-column>
        <el-table-column label="Class" width="150">
          <template #default="{ row }">
            <span class="top-class">{{ getClassEmoji(row.predicted_class) }} {{ formatClassName(row.predicted_class) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Confidence" width="150" sortable>
          <template #default="{ row }">
            <el-progress :percentage="row.confidence" :show-text="false" style="width: 100%; margin-right: 10px"></el-progress>
            {{ row.confidence }}%
          </template>
        </el-table-column>
        <el-table-column label="Top 3 Scores" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="top-scores">
              <span v-for="(score, i) in getTopScores(row.all_scores, 3)" :key="i" class="score-badge">
                {{ score }}
              </span>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePredictionStore } from '@/stores/predictionStore'

const store = usePredictionStore()

const predictions = computed(() => store.predictions)
const totalPredictions = computed(() => store.totalPredictions)
const classificationStats = computed(() => store.classificationStats)
const averageConfidence = computed(() => store.averageConfidence)

const modelMetrics = [
  { label: 'Validation Accuracy', value: 92.88, precision: 2, subtitle: 'on TrashNet dataset' },
  { label: 'Supported Classes', value: 6, precision: 0, subtitle: 'waste categories' },
  { label: 'Total Predictions', value: totalPredictions, precision: 0, subtitle: 'in this session' },
  { label: 'Avg. Confidence', value: averageConfidence, precision: 2, subtitle: 'from predictions' }
]

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

const getClassPercentage = (count: number): number => {
  if (totalPredictions.value === 0) return 0
  return Math.round((count / totalPredictions.value) * 100)
}

const statsTable = computed(() => [
  { metric: 'Total Predictions', value: totalPredictions.value },
  { metric: 'Average Confidence', value: averageConfidence.value + '%' },
  { metric: 'Most Common Class', value: getMostCommonClass() },
  { metric: 'Least Common Class', value: getLeastCommonClass() },
  { metric: 'High Confidence (≥90%)', value: highConfidenceCount.value },
  { metric: 'Low Confidence (<70%)', value: lowConfidenceCount.value }
])

const getMostCommonClass = (): string => {
  if (Object.keys(classificationStats.value).length === 0) return 'N/A'
  const entries = Object.entries(classificationStats.value)
  const [mostCommon] = entries.reduce((max, current) => (current[1] > max[1] ? current : max))
  return formatClassName(mostCommon)
}

const getLeastCommonClass = (): string => {
  if (Object.keys(classificationStats.value).length === 0) return 'N/A'
  const entries = Object.entries(classificationStats.value)
  const [leastCommon] = entries.reduce((min, current) => (current[1] < min[1] ? current : min))
  return formatClassName(leastCommon)
}

const highConfidenceCount = computed(() => {
  return predictions.value.filter((p) => p.confidence >= 90).length
})

const lowConfidenceCount = computed(() => {
  return predictions.value.filter((p) => p.confidence <= 70).length
})

const confidenceRanges = computed(() => {
  const ranges = [
    { label: '90-100%', min: 90, max: 100, color: '#67c23a' },
    { label: '80-89%', min: 80, max: 89, color: '#85ce61' },
    { label: '70-79%', min: 70, max: 79, color: '#e6a23c' },
    { label: '60-69%', min: 60, max: 69, color: '#f56c6c' },
    { label: '<60%', min: 0, max: 59, color: '#909399' }
  ]

  return ranges.map((range) => {
    const count = predictions.value.filter((p) => p.confidence >= range.min && p.confidence <= range.max).length
    const percentage = totalPredictions.value > 0 ? (count / totalPredictions.value) * 100 : 0
    return { ...range, count, percentage }
  })
})

const topPredictions = computed(() => {
  return [...predictions.value].sort((a, b) => b.confidence - a.confidence).slice(0, 10)
})

const getTopScores = (scores: { [key: string]: number }, limit: number): string[] => {
  return Object.entries(scores)
    .sort(([, a], [, b]) => b - a)
    .slice(0, limit)
    .map(([name, score]) => `${formatClassName(name)}: ${score.toFixed(1)}%`)
}
</script>

<style scoped lang="css">
.metrics-page {
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

.mt-30 {
  margin-top: 30px;
}

.metric-card {
  text-align: center;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.metric-card :deep(.el-statistic__content) {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.metric-subtitle {
  color: #999;
  font-size: 14px;
  margin-top: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.chart-container {
  min-height: 300px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-state p {
  margin: 0;
}

.empty-state a {
  color: #409eff;
  text-decoration: none;
}

.empty-state a:hover {
  text-decoration: underline;
}

.distribution-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.distribution-item {
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.distribution-item:hover {
  border-color: #409eff;
  background: #f0f9ff;
}

.distribution-emoji {
  font-size: 32px;
  margin-bottom: 10px;
}

.distribution-item h4 {
  margin: 10px 0 5px 0;
  color: #2c3e50;
  font-size: 16px;
}

.distribution-count {
  color: #999;
  font-size: 14px;
  margin: 5px 0;
}

.confidence-histogram {
  padding: 20px 0;
}

.confidence-histogram h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.histogram-bars {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.histogram-bar {
  display: grid;
  grid-template-columns: 80px 1fr 50px;
  gap: 15px;
  align-items: center;
}

.bar-label {
  text-align: center;
  font-weight: 600;
  color: #666;
  font-size: 14px;
}

.bar-container {
  background: #f0f0f0;
  border-radius: 8px;
  height: 30px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 10px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.bar-value {
  text-align: center;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.top-class {
  display: flex;
  align-items: center;
  gap: 8px;
}

.top-scores {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.score-badge {
  display: inline-block;
  padding: 4px 8px;
  background: #f0f9ff;
  color: #0081ff;
  border-radius: 4px;
  font-size: 12px;
}

@media (max-width: 768px) {
  .distribution-grid {
    grid-template-columns: 1fr;
  }

  .histogram-bar {
    grid-template-columns: 60px 1fr 50px;
    font-size: 12px;
  }
}
</style>
