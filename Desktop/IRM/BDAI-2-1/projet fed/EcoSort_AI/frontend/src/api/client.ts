import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000
})

// Prediction API
export const predictionAPI = {
  async predict(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    
    return apiClient.post('/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  async getHealth() {
    return apiClient.get('/health')
  },

  async getModelInfo() {
    return apiClient.get('/model/info')
  },

  async getClasses() {
    return apiClient.get('/classes')
  }
}

// Error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 503) {
      console.error('Service unavailable - Model not loaded')
    }
    return Promise.reject(error)
  }
)
