import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import { includedRoutes } from './src/ssg/includedRoutes.js'

export default defineConfig({
  plugins: [vue()],
  define: {
    __VUE_I18N_FULL_INSTALL__: true,
    __VUE_I18N_LEGACY_API__: false,
    __INTLIFY_PROD_DEVTOOLS__: false,
    // Absolute API base used only during SSG prerender (Node has no relative
    // URL host). The browser keeps using the relative VITE_API_BASE_URL.
    __SSG_API_BASE__: JSON.stringify(
      `${process.env.SSG_ORIGIN || 'https://thetadabbur.org'}/api/v1`,
    ),
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
  // vite-ssg: prerender each public route to static HTML. Route list comes from
  // the production sitemap (see src/ssg/includedRoutes.js). 'nested' emits
  // <route>/index.html so nginx can serve deep links directly.
  ssgOptions: {
    dirStyle: 'nested',
    formatting: 'minify',
    includedRoutes,
  },
})
