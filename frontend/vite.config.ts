import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

const isDocker = Boolean(process.env.IS_DOCKER)

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  envDir: './',
  envPrefix: 'VITE_',
  server: {
    // Containerized dev runs behind nginx in CI/local compose, so HMR is disabled there.
    hmr: isDocker ? false : {
      host: 'localhost',
      port: 3001
    }
  }
})
