// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'   // JSX & Fast Refresh

export default defineConfig({
  plugins: [react()],
  base: '/music-viewer/',                  // ← exact repo name
})
