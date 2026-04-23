import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/classify',
      name: 'Classify',
      component: () => import('@/views/Classify.vue')
    },
    {
      path: '/metrics',
      name: 'Metrics',
      component: () => import('@/views/Metrics.vue')
    },
    {
      path: '/impact',
      name: 'Impact',
      component: () => import('@/views/Impact.vue')
    }
  ]
})

export default router
