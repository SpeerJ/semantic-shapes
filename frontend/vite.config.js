import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ command }) => {
  const isDev = command === 'serve';
  const isProd = command === 'build';

  return {
  plugins: [react()],
  server: isDev ? {
    proxy: {
      '/api': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        secure: false,
      }
    }
  } : {},
    build: isProd ? {
      minify: 'terser',
      sourcemap: false,
    } : {}
}});
