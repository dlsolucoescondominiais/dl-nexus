import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build' // Muitas plataformas como Cloudflare Pages e React Create App assumem 'build' por padrão
  }
})
