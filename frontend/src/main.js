import { ViteSSG } from 'vite-ssg'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css'

import App from './App.vue'
import { routes, scrollBehavior, setupRouterGuards } from './router'
import { i18n } from './i18n'
import './assets/main.css'

// vite-ssg drives both the prerender (server) and the hydrated app (client)
// from this single exported factory. It creates the router + unhead instance
// itself; we only register the remaining plugins and wire Pinia state transfer.
export const createApp = ViteSSG(
  App,
  { routes, scrollBehavior },
  ({ app, router, initialState }) => {
    const pinia = createPinia()
    app.use(pinia)

    // State transfer for SSG hydration. On the server we snapshot the full
    // reactive state by reference (onServerPrefetch fills it during render). On
    // the client we restore ONLY the ssrData cache (plain JSON), so prerendered
    // content hydrates without a refetch. Client-only stores (auth, progress)
    // deliberately re-initialize fresh — progress holds a Set that wouldn't
    // survive JSON serialization, and both are per-user, not build-time data.
    if (import.meta.env.SSR) {
      initialState.pinia = pinia.state.value
    } else if (initialState.pinia?.ssrData) {
      pinia.state.value.ssrData = initialState.pinia.ssrData
    }

    app.use(i18n)
    app.use(PrimeVue, {
      theme: {
        preset: Aura,
        options: { darkModeSelector: '.dark' },
      },
    })

    setupRouterGuards(router)
  },
)
