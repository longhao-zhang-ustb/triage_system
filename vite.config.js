import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: './',
  plugins: [vue()],
  server: {
    port: 3051,
    proxy: {
      '/api': {
        target: 'http://localhost:8014',
        changeOrigin: true
      },
      '/match-api': {
        target: 'http://localhost:5800',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/match-api/, '')
      },
      '/analyzer-api': {
        target: 'http://localhost:6800',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/analyzer-api/, '')
      },
      '/device-api': {
        target: 'http://localhost:7851',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/device-api/, '')
      }
    }
  }
})
