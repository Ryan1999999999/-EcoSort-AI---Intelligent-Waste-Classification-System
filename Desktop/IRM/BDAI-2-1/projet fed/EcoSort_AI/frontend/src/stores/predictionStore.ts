import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface PredictionResult {
  predicted_class: string
  confidence: number
  all_scores: { [key: string]: number }
  impact_message: string
}

export const usePredictionStore = defineStore('prediction', () => {
  const predictions = ref<PredictionResult[]>([])
  const currentPrediction = ref<PredictionResult | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const totalPredictions = computed(() => predictions.value.length)

  const classificationStats = computed(() => {
    const stats: { [key: string]: number } = {}
    predictions.value.forEach((pred) => {
      stats[pred.predicted_class] = (stats[pred.predicted_class] || 0) + 1
    })
    return stats
  })

  const averageConfidence = computed(() => {
    if (predictions.value.length === 0) return 0
    const sum = predictions.value.reduce((acc, pred) => acc + pred.confidence, 0)
    return (sum / predictions.value.length).toFixed(2)
  })

  function addPrediction(prediction: PredictionResult) {
    predictions.value.push(prediction)
    currentPrediction.value = prediction
  }

  function clearPredictions() {
    predictions.value = []
    currentPrediction.value = null
  }

  function setError(message: string) {
    error.value = message
  }

  function clearError() {
    error.value = null
  }

  return {
    predictions,
    currentPrediction,
    loading,
    error,
    totalPredictions,
    classificationStats,
    averageConfidence,
    addPrediction,
    clearPredictions,
    setError,
    clearError
  }
})
