import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

function  isNotDocker() {
  const b = !process.env.IS_DOCKER
  console.log('isDocker:', b)
  return b
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
    // we do not need hmr in docker images + default address would not work (host: 'host.docker.internal' would be needed)
    hmr: isNotDocker(),
  }
})
