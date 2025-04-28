import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/blog': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
      '/account': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
      '/static': { 
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
      '/verify_email':{
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure:false,
      },
    },
  },
})
