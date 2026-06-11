import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => ({
  base: mode === 'production' ? '/taskhub/' : '/',
  plugins: [
    vue(),
    tailwindcss(),
  ],
  server: {
    host: 'localhost',
    port: 60001,
  }

}))