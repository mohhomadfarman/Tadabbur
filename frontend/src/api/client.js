import axios from 'axios'

// During SSG prerender (Node), relative URLs have no host, so point axios at an
// absolute origin (__SSG_API_BASE__, injected at build). In the browser, keep
// the relative base so requests stay same-origin behind nginx.
const baseURL = import.meta.env.SSR
  ? __SSG_API_BASE__
  : import.meta.env.VITE_API_BASE_URL || '/api/v1'

const client = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

// SSG prerender runs these interceptors in Node (no localStorage/window), so
// guard browser access. Prerender only fetches public data — no token needed.
const isClient = typeof window !== 'undefined'

// Attach JWT to every request
client.interceptors.request.use((config) => {
  const token = isClient ? localStorage.getItem('access_token') : null
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auto-refresh on 401
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (isClient && error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          const { data } = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL || '/api/v1'}/auth/token/refresh/`,
            { refresh }
          )
          localStorage.setItem('access_token', data.access)
          original.headers.Authorization = `Bearer ${data.access}`
          return client.request(original)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default client
