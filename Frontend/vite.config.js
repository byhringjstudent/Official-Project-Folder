import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  base: '/',
  plugins: [react(), tailwindcss()],
  server: {
    historyApiFallback: true, 
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/verify_email': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/static/uploads': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/static/react_build/assets': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})