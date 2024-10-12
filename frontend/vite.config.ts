import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

function getHmrHost() {
  return process.env.IS_DOCKER ? 'host.docker.internal' : 'localhost'
}

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
  define: { // in order for env variables to be reliably available in the docker container
    'process.env': process.env
  },
  server: {
    // in order for hot module replacement to not throw an error inside the docker container
    // (localhost would resolve to the container and not the host)
    hmr: {
      host: getHmrHost(),
      port: 3001
    }
  }
})
