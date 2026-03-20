import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    host: '0.0.0.0',
    port: 5000,
    allowedHosts: 'all',
    watch: {
      ignored: ['**/.pythonlibs/**', '**/models/**', '**/data/**', '**/__pycache__/**'],
    },
    proxy: {
      '/predict-symptom': 'http://localhost:8000',
      '/predict-image': 'http://localhost:8000',
      '/api': 'http://localhost:8000',
    },
  },
});
