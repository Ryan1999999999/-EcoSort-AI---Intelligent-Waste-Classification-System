<template>
  <div id="app" class="app">
    <el-container class="layout">
      <!-- Header -->
      <el-header class="header" height="70px">
        <div class="header-content">
          <div class="logo">
            <span class="logo-text">♻️ EcoSort AI</span>
          </div>
          <el-menu 
            :default-active="activeMenu" 
            mode="horizontal" 
            router
            class="nav-menu"
          >
            <el-menu-item index="0" route="/">Home</el-menu-item>
            <el-menu-item index="1" route="/classify">Classify</el-menu-item>
            <el-menu-item index="2" route="/metrics">Metrics</el-menu-item>
            <el-menu-item index="3" route="/impact">Impact</el-menu-item>
          </el-menu>
        </div>
      </el-header>

      <!-- Main Content -->
      <el-main class="main">
        <router-view></router-view>
      </el-main>

      <!-- Footer -->
      <el-footer class="footer" height="60px">
        <div class="footer-content">
          <p>&copy; 2024 EcoSort AI - Intelligent Waste Classification</p>
          <p class="version">v1.0.0</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { predictionAPI } from '@/api/client'

const route = useRoute()
const activeMenu = ref('0')

onMounted(async () => {
  try {
    await predictionAPI.getHealth()
    ElMessage.success('Backend connected successfully!')
  } catch (error) {
    ElMessage.error('Failed to connect to backend. Make sure it is running on port 8000.')
  }
})
</script>

<style scoped lang="css">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  padding: 0 20px !important;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  height: 100%;
}

.logo-text {
  font-size: 28px;
  font-weight: bold;
  color: #fff;
  letter-spacing: 1px;
}

.nav-menu {
  background: transparent !important;
  border: none !important;
  height: 100%;
  display: flex;
  align-items: center;
}

.nav-menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.8) !important;
  border-bottom: none !important;
  font-weight: 500 !important;
}

.nav-menu :deep(.el-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
}

.nav-menu :deep(.el-menu-item.is-active) {
  background-color: transparent !important;
  color: #00ff88 !important;
  border-bottom: 3px solid #00ff88 !important;
}

.main {
  flex: 1;
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
  color: rgba(255, 255, 255, 0.8);
  padding: 0 20px !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  text-align: center;
  font-size: 14px;
}

.footer-content p {
  margin: 5px 0;
}

.version {
  color: #00ff88 !important;
  font-weight: bold;
}

@media (max-width: 768px) {
  .header {
    padding: 0 10px !important;
  }

  .logo-text {
    font-size: 20px;
  }

  .main {
    padding: 15px;
  }
}
</style>
