<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import TriageMain from './components/TriageMain.vue'

// 路由状态
const currentRoute = ref(window.location.hash.slice(1) || '/')

// 监听hash变化
const handleHashChange = () => {
  currentRoute.value = window.location.hash.slice(1) || '/'
}

// 导航函数
const navigateTo = (path) => {
  window.location.hash = path
}

// 组件挂载时添加监听器
onMounted(() => {
  window.addEventListener('hashchange', handleHashChange)
})

// 组件卸载时移除监听器
onUnmounted(() => {
  window.removeEventListener('hashchange', handleHashChange)
})
</script>

<template>
  <div id="app">
    <TriageMain v-if="currentRoute === '/'" :navigate-to="navigateTo" />
    <div v-else class="not-found">
      <h1>Page Not Found</h1>
      <button @click="navigateTo('/')">Return to Home</button>
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: linear-gradient(135deg, #f2f9f8 0%, #e0f2f1 100%);
  font-family: 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  color:rgb(100, 133, 167);
  line-height: 1.6;
}

#app {
  height: 100vh;
  width: 100vw;
}

.not-found {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: white;
  text-align: center;
}

.not-found h1 {
  font-size: 3rem;
  margin-bottom: 2rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.not-found button {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.not-found button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}
</style>
