<template>
  <div class="impact-page">
    <!-- Environmental Impact Overview -->
    <el-row :gutter="20" class="mb-30">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card class="impact-card">
          <template #header>
            <div class="card-header">
              <span>🌍 Why Recycling Matters</span>
            </div>
          </template>
          <div class="impact-content">
            <h3>Environmental Impact Statistics</h3>
            <ul class="impact-list">
              <li>♻️ Recycling reduces new raw material production by 90%</li>
              <li>💧 Saves 2,700+ liters of water per recycled ton of plastic</li>
              <li>⚡ Uses 95% less energy than mining new materials</li>
              <li>🌳 Saves 24 trees per ton of recycled cardboard</li>
              <li>🔗 Aluminum can be recycled infinitely without degradation</li>
              <li>♾️ Takes 400+ years for plastic to decompose</li>
            </ul>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card class="impact-card">
          <template #header>
            <div class="card-header">
              <span>📊 Recycling Rate by Country</span>
            </div>
          </template>
          <el-table :data="recyclingRates" stripe style="width: 100%">
            <el-table-column prop="country" label="Country" width="120"></el-table-column>
            <el-table-column prop="rate" label="Rate" width="80">
              <template #default="{ row }">
                <el-progress :percentage="row.rate" :show-text="false" style="width: 80px"></el-progress>
              </template>
            </el-table-column>
            <el-table-column prop="rateLabel" label="" width="60"></el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- Waste Category Impact -->
    <el-card class="mb-30">
      <template #header>
        <div class="card-header">
          <span>🗑️ Waste Category Impact</span>
        </div>
      </template>

      <el-empty v-if="totalPredictions === 0" :image-size="100" description="No predictions yet">
        <router-link to="/classify" class="empty-link">Make a prediction to see impact</router-link>
      </el-empty>

      <el-row v-else :gutter="20">
        <el-col
          v-for="(count, className) in classificationStats"
          :key="className"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
          class="mb-20"
        >
          <div class="impact-category">
            <div class="category-emoji">{{ getClassEmoji(className) }}</div>
            <h4>{{ formatClassName(className) }}</h4>
            <div class="category-count">
              <el-statistic :value="count" suffix="classified"></el-statistic>
            </div>
            <div class="category-impact">
              <p class="impact-text">{{ getCategoryImpact(className) }}</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- Your Impact Summary -->
    <el-card class="mb-30" v-if="totalPredictions > 0">
      <template #header>
        <div class="card-header">
          <span>🎯 Your Impact Summary</span>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <div class="impact-stat">
            <div class="stat-number">{{ totalPredictions }}</div>
            <div class="stat-label">Items Classified</div>
            <div class="stat-icon">📋</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <div class="impact-stat">
            <div class="stat-number">{{ classificationStats['cardboard'] || 0 }}</div>
            <div class="stat-label">Cardboard Items</div>
            <div class="stat-icon">📦</div>
            <div class="stat-savings">Saving {{ (classificationStats['cardboard'] || 0) * 5 }} liters of water</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <div class="impact-stat">
            <div class="stat-number">{{ classificationStats['plastic'] || 0 }}</div>
            <div class="stat-label">Plastic Items</div>
            <div class="stat-icon">🥤</div>
            <div class="stat-savings">Preventing 400+ years of landfill</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <div class="impact-stat">
            <div class="stat-number">{{ classificationStats['metal'] || 0 }}</div>
            <div class="stat-label">Metal Items</div>
            <div class="stat-icon">🔗</div>
            <div class="stat-savings">Saving 95% energy</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- Detailed Impact Information -->
    <el-card class="mb-30">
      <template #header>
        <div class="card-header">
          <span>📚 Detailed Impact Information</span>
        </div>
      </template>

      <el-collapse>
        <el-collapse-item v-for="category in allCategories" :key="category.name" :title="`${category.emoji} ${category.name}`" :name="category.name">
          <div class="category-details">
            <h4>{{ category.emoji }} {{ category.name }}</h4>
            <div class="detail-section">
              <h5>♻️ Recyclability</h5>
              <p>{{ category.recyclability }}</p>
            </div>
            <div class="detail-section">
              <h5>🌍 Environmental Impact</h5>
              <p>{{ category.impact }}</p>
            </div>
            <div class="detail-section">
              <h5>✅ How to Dispose</h5>
              <p>{{ category.disposal }}</p>
            </div>
            <div class="detail-section">
              <h5>💰 Economic Value</h5>
              <p>{{ category.economic }}</p>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- UN Sustainable Development Goals -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>🎯 UN Sustainable Development Goals</span>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col v-for="goal in sdgGoals" :key="goal.number" :xs="24" :sm="12" :md="8" :lg="6" class="mb-20">
          <div class="sdg-goal">
            <div class="goal-number">{{ goal.number }}</div>
            <h4>{{ goal.title }}</h4>
            <p>{{ goal.description }}</p>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePredictionStore } from '@/stores/predictionStore'

const store = usePredictionStore()

const totalPredictions = computed(() => store.totalPredictions)
const classificationStats = computed(() => store.classificationStats)

const classEmojiMap: { [key: string]: string } = {
  'cardboard': '📦',
  'glass': '🍾',
  'metal': '🔗',
  'paper': '📄',
  'plastic': '🥤',
  'trash': '🗑️'
}

const categoryImpactMessages: { [key: string]: string } = {
  'cardboard': 'Recycling one ton of cardboard saves 24 trees and 4,000 gallons of water.',
  'glass': 'One recycled glass bottle saves enough energy to power a laptop for 3 hours.',
  'metal': 'Recycling aluminum uses 95% less energy than mining new material.',
  'paper': 'After 7 recycling cycles, paper fibers become too short. Reduce consumption when possible.',
  'plastic': 'Only ~9% of plastic has been recycled. Most takes 400+ years to decompose.',
  'trash': 'Items in this category should be minimized. Reduce consumption overall.'
}

const recyclingRates = [
  { country: 'Germany', rate: 66, rateLabel: '66%' },
  { country: 'Austria', rate: 63, rateLabel: '63%' },
  { country: 'Belgium', rate: 58, rateLabel: '58%' },
  { country: 'Netherlands', rate: 55, rateLabel: '55%' },
  { country: 'France', rate: 44, rateLabel: '44%' },
  { country: 'USA', rate: 32, rateLabel: '32%' }
]

const allCategories = [
  {
    name: 'Cardboard',
    emoji: '📦',
    recyclability: 'Highly recyclable. Can be processed 5-7 times before fibers degrade.',
    impact: 'Recycling one ton saves 24 trees and 4,000 gallons of water. Reduces deforestation.',
    disposal: 'Flatten boxes, keep dry, remove plastic. Can be placed in recycling bins.',
    economic: 'Average return of $0.50-1.50 per pound depending on market and quality.'
  },
  {
    name: 'Glass',
    emoji: '🍾',
    recyclability: '100% recyclable and can be reused indefinitely without degradation.',
    impact: 'One recycled glass bottle saves energy equal to powering a laptop for 3 hours.',
    disposal: 'Rinse thoroughly, separate by color if facility requires. Handle carefully to prevent breakage.',
    economic: 'Lower economic value but essential for reducing landfill waste.'
  },
  {
    name: 'Metal',
    emoji: '🔗',
    recyclability: 'Infinitely recyclable without loss of quality or properties.',
    impact: 'Recycling aluminum uses 95% less energy than mining new metal.',
    disposal: 'Rinse food containers, flatten to save space, keep separate from other materials.',
    economic: 'Aluminum cans average 1-2 cents per can in most recycling programs.'
  },
  {
    name: 'Paper',
    emoji: '📄',
    recyclability: 'Recyclable but only 7 times before fibers become too short.',
    impact: 'Reduces demand for new trees. However, reducing consumption is even better.',
    disposal: 'Keep dry, remove plastic coating, bundle newspapers if possible.',
    economic: 'Shredded paper is often mixed with other recyclables for lower value.'
  },
  {
    name: 'Plastic',
    emoji: '🥤',
    recyclability: 'Only ~9% of all plastic ever produced has been recycled.',
    impact: 'Most plastics take 400+ years to decompose. Persistence in environment is major issue.',
    disposal: 'Rinse bottles, codes 1 & 2 are most recyclable. Check local guidelines.',
    economic: 'Limited value; focus should be on reduction and reuse over recycling.'
  },
  {
    name: 'Trash',
    emoji: '🗑️',
    recyclability: 'General waste that cannot be recycled.',
    impact: 'Contributes to landfill waste and environmental degradation.',
    disposal: 'Final destination is landfill. Minimize production of this category.',
    economic: 'No economic value. Focus on separating recyclables instead.'
  }
]

const sdgGoals = [
  {
    number: '7',
    title: 'Affordable & Clean Energy',
    description: 'Recycling reduces energy consumption by up to 95% compared to primary production.'
  },
  {
    number: '11',
    title: 'Sustainable Cities',
    description: 'Better waste management creates cleaner, healthier communities.'
  },
  {
    number: '12',
    title: 'Responsible Consumption',
    description: 'Sustainable production and consumption patterns reduce waste.'
  },
  {
    number: '13',
    title: 'Climate Action',
    description: 'Reduced production emissions through recycling help combat climate change.'
  },
  {
    number: '14',
    title: 'Life Below Water',
    description: 'Proper recycling prevents plastic pollution in oceans.'
  },
  {
    number: '15',
    title: 'Life on Land',
    description: 'Conservation of forests and ecosystems through responsible resource use.'
  }
]

const getClassEmoji = (className: string): string => {
  return classEmojiMap[className] || '📌'
}

const formatClassName = (name: string): string => {
  return name.charAt(0).toUpperCase() + name.slice(1)
}

const getCategoryImpact = (className: string): string => {
  return categoryImpactMessages[className] || 'No specific impact data'
}
</script>

<style scoped lang="css">
.impact-page {
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

.impact-card {
  height: 100%;
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

.impact-content {
  animation: slideDown 0.5s ease-in;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.impact-content h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.impact-list {
  list-style: none;
  padding: 0;
}

.impact-list li {
  padding: 10px 0;
  color: #555;
  line-height: 1.6;
  border-bottom: 1px solid #eee;
}

.impact-list li:last-child {
  border-bottom: none;
}

.impact-category {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.impact-category:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.category-emoji {
  font-size: 48px;
  margin-bottom: 15px;
}

.impact-category h4 {
  color: #2c3e50;
  margin: 10px 0;
  font-size: 18px;
}

.category-count {
  margin: 15px 0;
}

.category-count :deep(.el-statistic__content) {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

.impact-text {
  color: #666;
  font-size: 13px;
  line-height: 1.4;
  margin: 0;
  font-weight: 500;
}

.impact-stat {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  color: white;
  transition: all 0.3s ease;
}

.impact-stat:hover {
  transform: scale(1.05);
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
}

.stat-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.stat-savings {
  font-size: 12px;
  margin-top: 10px;
  opacity: 0.9;
  font-style: italic;
}

.category-details {
  padding: 20px 0;
}

.category-details h4 {
  color: #2c3e50;
  font-size: 20px;
  margin-bottom: 20px;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h5 {
  color: #409eff;
  margin-bottom: 10px;
  font-size: 16px;
}

.detail-section p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.sdg-goal {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  color: white;
  transition: all 0.3s ease;
  height: 100%;
}

.sdg-goal:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(245, 87, 108, 0.4);
}

.goal-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
  background: rgba(255, 255, 255, 0.2);
  padding: 10px;
  border-radius: 8px;
  display: inline-block;
}

.sdg-goal h4 {
  font-size: 16px;
  margin: 15px 0 10px 0;
}

.sdg-goal p {
  font-size: 13px;
  line-height: 1.4;
  margin: 0;
}

.empty-link {
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}

.empty-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .impact-category, .impact-stat, .sdg-goal {
    padding: 15px;
  }

  .category-emoji, .stat-icon {
    font-size: 32px;
  }

  .stat-number {
    font-size: 24px;
  }
}
</style>
