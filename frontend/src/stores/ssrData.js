import { defineStore } from 'pinia'

// Ferries data fetched during SSG prerender (onServerPrefetch) to the browser.
// vite-ssg serializes Pinia state into the page (window.__INITIAL_STATE__), so a
// view can hydrate its first client render from cache[key] — matching the
// prerendered HTML exactly (no hydration mismatch) — and then refetch in the
// background for fresh/personalized data when needed.
//
// Each prerendered page renders in its own app/Pinia instance, so a page's
// serialized cache only ever contains that page's own data.
export const useSsrDataStore = defineStore('ssrData', {
  state: () => ({ cache: {} }),
  actions: {
    set(key, value) {
      this.cache[key] = value
    },
    get(key) {
      return this.cache[key] ?? null
    },
  },
})
